import pandas as pd

def read_csv_data(filepath):
    try:
        df = pd.read_csv(filepath)
        print("[INFO] CSV data loaded successfully.")
        return df
    except Exception as e:
        print(f"[ERROR] Failed to read CSV: {e}")
        return pd.DataFrame()  # return empty DataFrame if error

