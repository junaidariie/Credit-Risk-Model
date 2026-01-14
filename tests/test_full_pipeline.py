import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.train import train_pipeline
from src.evaluate import evaluate_model

def test_full_pipeline():
    model_path, scaler_path, columns_path = train_pipeline()
    evaluate_model(model_path, scaler_path, columns_path)

    print("Full pipeline test passed end-to-end.")

if __name__ == "__main__":
    test_full_pipeline()

