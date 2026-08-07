import joblib
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.model_selection import train_test_split

from src.ingestion import load_raw_data
from src.preprocessing import clean_and_engineer
from src.utils import load_config


def evaluate_model(artifact_path):
    model_data = joblib.load(artifact_path)
    model = model_data["model"]
    scaler = model_data["scaler"]
    columns = model_data["features"]

    config = load_config()
    target = config["data"]["target"]

    df = load_raw_data()
    df = clean_and_engineer(df)

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

    X_test = X_test.reindex(columns=columns, fill_value=0)
    X_scaled = scaler.transform(X_test)

    preds_proba = model.predict_proba(X_scaled)[:, 1]
    threshold = 0.85
    preds = (preds_proba >= threshold).astype(int)

    auc = roc_auc_score(y_test, preds_proba)
    accuracy = accuracy_score(y_test, preds)
    precision = precision_score(y_test, preds, zero_division=0)
    recall = recall_score(y_test, preds, zero_division=0)
    f1 = f1_score(y_test, preds, zero_division=0)

    print("Accuracy:", accuracy)
    print("Precision:", precision)
    print("Recall:", recall)
    print("F1:", f1)
    print("AUC:", auc)
    return auc

