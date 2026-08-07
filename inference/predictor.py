import math
import pandas as pd
import numpy as np
import joblib

from src.preprocessing import clean_and_engineer


class CreditRiskPredictor:
    def __init__(self, model_path="artifacts/model_data.joblib"):
        self.model_path = model_path

        model_data = joblib.load(self.model_path)
        self.model = model_data["model"]
        self.scaler = model_data["scaler"]
        self.columns = model_data["features"]

    def predict(self, input_dict: dict):
        df = pd.DataFrame([input_dict])
        df = clean_and_engineer(df)
        df = pd.get_dummies(df, drop_first=True)

        missing_cols = [col for col in self.columns if col not in df.columns]
        extra_cols = [col for col in df.columns if col not in self.columns]

        if missing_cols:
            for col in missing_cols:
                df[col] = 0

        if extra_cols:
            df = df.drop(columns=extra_cols)

        df = df.reindex(columns=self.columns, fill_value=0)

        X_scaled = self.scaler.transform(df)

        probability, credit_score, rating = self._calculate_scorecard_output(
            X_scaled
        )

        probability = round(probability, 4)

        return probability, credit_score, rating

    def _calculate_scorecard_output(
        self,
        X_scaled,
        base_score=600,
        base_odds=50,
        pdo=20,
    ):
        # Logistic Regression raw score
        x = np.dot(X_scaled, self.model.coef_.T) + self.model.intercept_

        # Probability of Default
        default_probability = 1 / (1 + np.exp(-x))
        default_probability = float(default_probability.flatten()[0])

        # Prevent division by zero
        default_probability = min(max(default_probability, 1e-6), 1 - 1e-6)

        # Probability of Non-Default
        non_default_probability = 1 - default_probability

        # Good / Bad Odds
        odds = non_default_probability / default_probability

        # Industry-standard scorecard parameters
        factor = pdo / math.log(2)
        offset = base_score - factor * math.log(base_odds)

        # Credit Score
        credit_score = offset + factor * math.log(odds)

        # Clamp to 300-900
        credit_score = int(round(max(300, min(900, credit_score))))

        rating = self._get_rating(credit_score)

        return default_probability, credit_score, rating

    def _get_rating(self, score):
        if 300 <= score < 500:
            return "Poor"
        elif 500 <= score < 650:
            return "Average"
        elif 650 <= score < 750:
            return "Good"
        elif 750 <= score <= 900:
            return "Excellent"
        else:
            return "Undefined"