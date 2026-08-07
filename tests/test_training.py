import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.train import train_pipeline

def test_training():
    artifact_path = train_pipeline()

    assert os.path.exists(artifact_path), "Model artifact file not created"

    print("Training test passed.")
    print("Artifact:", artifact_path)

if __name__ == "__main__":
    test_training()
