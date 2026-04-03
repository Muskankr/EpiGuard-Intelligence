def get_risk_level(daily_cases_series):
    latest = daily_cases_series.iloc[-1]

    if latest < 100:
        return "🟢 Low Risk"
    elif latest < 1000:
        return "🟡 Medium Risk"
    else:
        return "🔴 High Risk"