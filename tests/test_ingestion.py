import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.ingestion import load_raw_data

def test_ingestion():
    df = load_raw_data()

    assert df is not None, "DataFrame is None"
    assert df.shape[0] > 0, "No rows loaded"
    assert "cust_id" in df.columns, "cust_id missing"
    assert "loan_amount" in df.columns, "loan_amount missing"

    print("Ingestion test passed. Shape:", df.shape)

if __name__ == "__main__":
    test_ingestion()
