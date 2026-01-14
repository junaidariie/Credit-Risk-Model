import joblib
import pandas as pd
from sklearn.metrics import roc_auc_score

from src.ingestion import load_raw_data
from src.preprocessing import clean_and_engineer


def evaluate_model(model_path, scaler_path, columns_path):
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    columns = joblib.load(columns_path)

    df = load_raw_data()
    df = clean_and_engineer(df)

    X = df.drop("default", axis=1)
    y = df["default"]

    X = pd.get_dummies(X, drop_first=True)

    X = X.reindex(columns=columns, fill_value=0)

    X_scaled = scaler.transform(X)

    preds = model.predict_proba(X_scaled)[:, 1]
    auc = roc_auc_score(y, preds)

    print("AUC:", auc)
    return auc
