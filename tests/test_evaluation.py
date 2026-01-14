import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.train import train_pipeline
from src.evaluate import evaluate_model

def test_evaluation():
    model_path, scaler_path, columns_path = train_pipeline()

    auc = evaluate_model(model_path, scaler_path, columns_path)

    assert auc > 0.5, "AUC too low"
    print("Evaluation test passed. AUC:", auc)

if __name__ == "__main__":
    test_evaluation()
