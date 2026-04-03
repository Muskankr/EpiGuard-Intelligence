def make_prediction(model, days=14):
    """
    Predict future cases
    """
    future = model.make_future_dataframe(periods=days)
    forecast = model.predict(future)

    return forecast