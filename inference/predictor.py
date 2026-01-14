import pandas as pd
import numpy as np
import joblib

from src.utils import get_latest_file
from src.preprocessing import clean_and_engineer

MODEL_DIR = "models"


class CreditRiskPredictor:
    def __init__(self):
        self.model_path = get_latest_file(MODEL_DIR, "credit_model")
        self.scaler_path = get_latest_file(MODEL_DIR, "scaler")
        self.columns_path = get_latest_file(MODEL_DIR, "columns")

        self.model = joblib.load(self.model_path)
        self.scaler = joblib.load(self.scaler_path)
        self.columns = joblib.load(self.columns_path)

    def predict(self, input_dict: dict):
        df = pd.DataFrame([input_dict])
        df = clean_and_engineer(df)
        df = pd.get_dummies(df, drop_first=True)
        df = df.reindex(columns=self.columns, fill_value=0)
        X_scaled = self.scaler.transform(df)

        probability, credit_score, rating = self._calculate_scorecard_output(X_scaled)

        probability = round(probability, 4)

        return probability, credit_score, rating

    def _calculate_scorecard_output(self, X_scaled, base_score=300, scale_length=600):
        x = np.dot(X_scaled, self.model.coef_.T) + self.model.intercept_
        default_probability = 1 / (1 + np.exp(-x))
        non_default_probability = 1 - default_probability
        credit_score = base_score + non_default_probability.flatten() * scale_length
        credit_score = int(credit_score[0])
        rating = self._get_rating(credit_score)

        return float(default_probability.flatten()[0]), credit_score, rating

    def _get_rating(self, score):
        if 300 <= score < 500:
            return 'Poor'
        elif 500 <= score < 650:
            return 'Average'
        elif 650 <= score < 750:
            return 'Good'
        elif 750 <= score <= 900:
            return 'Excellent'
        else:
            return 'Undefined'
