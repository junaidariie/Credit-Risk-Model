import pandas as pd
from src.utils import load_config

def load_raw_data():
    config = load_config()
    customers = pd.read_csv(config["data"]["customers_path"])
    loans = pd.read_csv(config["data"]["loans_path"])
    bureau = pd.read_csv(config["data"]["bureau_path"])

    df = pd.merge(customers, loans, on="cust_id")
    df = pd.merge(df, bureau, on="cust_id")

    return df
