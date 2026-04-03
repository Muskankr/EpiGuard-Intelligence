from prophet import Prophet
import pandas as pd

def prepare_data_for_model(series):
    """
    Convert time series into Prophet format
    """
    df = series.reset_index()
    df.columns = ['ds', 'y']
    return df


def train_model(series):
    """
    Train Prophet model
    """
    df = prepare_data_for_model(series)

    model = Prophet(
        daily_seasonality=True,
        weekly_seasonality=True,
        yearly_seasonality=True
    )

    model.fit(df)

    return model