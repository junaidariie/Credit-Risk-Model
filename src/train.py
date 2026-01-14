import pandas as pd
import joblib
from sklearn.preprocessing import MinMaxScaler
from imblearn.combine import SMOTETomek
from sklearn.linear_model import LogisticRegression

from src.utils import load_config, get_versioned_path
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

    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X_encoded)

    smt = SMOTETomek(random_state=config["training"]["random_state"])
    X_res, y_res = smt.fit_resample(X_scaled, y)

    params = config["model"]["params"]
    model = LogisticRegression(**params)
    model.fit(X_res, y_res)

    model_path = get_versioned_path(config["artifacts"]["model_dir"], "credit_model", "pkl")
    scaler_path = get_versioned_path(config["artifacts"]["model_dir"], "scaler", "pkl")
    columns_path = get_versioned_path(config["artifacts"]["model_dir"], "columns", "pkl")

    joblib.dump(model, model_path)
    joblib.dump(scaler, scaler_path)
    joblib.dump(list(X_encoded.columns), columns_path)

    print(f"Model saved at: {model_path}")
    print(f"Scaler saved at: {scaler_path}")
    print(f"Columns saved at: {columns_path}")

    return model_path, scaler_path, columns_path


if __name__ == "__main__":
    train_pipeline()
