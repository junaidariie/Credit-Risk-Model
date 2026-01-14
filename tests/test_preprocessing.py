import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.ingestion import load_raw_data
from src.preprocessing import clean_and_engineer

def test_preprocessing():
    df = load_raw_data()
    processed = clean_and_engineer(df)

    assert processed is not None, "Processed DF is None"
    assert processed.shape[0] > 0, "No rows after preprocessing"
    assert "loan_to_income" in processed.columns, "loan_to_income not created"
    assert "avg_dpd_per_delinquency" in processed.columns, "avg_dpd_per_delinquency missing"

    assert "cust_id" not in processed.columns, "cust_id should be dropped"
    assert "loan_id" not in processed.columns, "loan_id should be dropped"

    print("Preprocessing test passed. Shape:", processed.shape)

if __name__ == "__main__":
    test_preprocessing()
