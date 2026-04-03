import pandas as pd
import numpy as np

def create_features(df):
    # 1. Daily cases
    daily_cases = df.diff().fillna(0)

    # 🔥 FIX: Avoid division by zero
    daily_cases_safe = daily_cases.replace(0, np.nan)

    # 2. Growth rate (safe calculation)
    growth_rate = daily_cases_safe.pct_change()

    # Replace NaN and inf values
    growth_rate = growth_rate.replace([np.inf, -np.inf], 0)
    growth_rate = growth_rate.fillna(0)

    # 3. Rolling average
    rolling_avg = daily_cases.rolling(window=7).mean().fillna(0)

    return daily_cases, growth_rate, rolling_avg