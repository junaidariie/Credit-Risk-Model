import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.train import train_pipeline

def test_training():
    model_path, scaler_path, columns_path = train_pipeline()

    assert os.path.exists(model_path), "Model file not created"
    assert os.path.exists(scaler_path), "Scaler file not created"
    assert os.path.exists(columns_path), "Columns file not created"

    print("Training test passed.")
    print("Model:", model_path)
    print("Scaler:", scaler_path)
    print("Columns:", columns_path)

if __name__ == "__main__":
    test_training()
