def simulate_cases(series, factor):
    """
    Simulate future cases based on a factor
    factor > 1 → increase spread
    factor < 1 → decrease spread
    """

    simulated = series.copy()

    # Apply factor to last 14 days
    simulated.iloc[-14:] = simulated.iloc[-14:] * factor

    return simulated