import os
import pandas as pd
import joblib
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from imblearn.combine import SMOTETomek
from sklearn.linear_model import LogisticRegression

from src.utils import load_config
from src.ingestion import load_raw_data
from src.preprocessing import clean_and_engineer


def train_pipeline():
    config = load_config()

    df = load_raw_data()
    df = clean_and_engineer(df)

    target = config["data"]["target"]

    X = df.drop(columns=[target])
    y = df[target]

    X_encoded = pd.get_dummies(X, drop_first=True)

    X_train, X_test, y_train, y_test = train_test_split(
        X_encoded,
        y,
        test_size=config["training"]["test_size"],
        random_state=config["training"]["random_state"],
        stratify=y,
    )

    scaler = MinMaxScaler()
    X_train_scaled = scaler.fit_transform(X_train)

    smt = SMOTETomek(random_state=config["training"]["random_state"])
    X_res, y_res = smt.fit_resample(X_train_scaled, y_train)

    params = config["model"]["params"]
    model = LogisticRegression(**params)
    model.fit(X_res, y_res)

    artifact_dir = os.path.join("artifacts")
    os.makedirs(artifact_dir, exist_ok=True)
    artifact_path = os.path.join(artifact_dir, "model_data.joblib")

    model_data = {
        "model": model,
        "scaler": scaler,
        "features": list(X_encoded.columns),
        "cols_to_scale": list(X_train.columns),
    }

    joblib.dump(model_data, artifact_path)

    print(f"Model artifact saved at: {artifact_path}")

    return artifact_path


if __name__ == "__main__":
    train_pipeline()
