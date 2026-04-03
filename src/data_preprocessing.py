import pandas as pd

def load_data(path):
    return pd.read_csv(path)


def preprocess_data(df):
    # Drop unwanted columns safely
    df = df.drop(columns=['Lat', 'Long'], errors='ignore')

    # Group by country
    df = df.groupby('Country/Region').sum()

    # Transpose
    df = df.T

    # 🔥 FIX: Remove non-date rows (VERY IMPORTANT)
    df = df[df.index.str.contains(r'\d')]  # keep only date rows

    # Convert to datetime
    df.index = pd.to_datetime(df.index)

    return df