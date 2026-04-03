import pandas as pd
import plotly.express as px

def create_heatmap(df, daily):
    latest_cases = daily.iloc[-1]

    # Convert to DataFrame
    heatmap_df = pd.DataFrame({
        "Country": latest_cases.index,
        "Cases": latest_cases.values
    })

    # Risk classification
    def classify_risk(x):
        if x < 100:
            return "Low"
        elif x < 1000:
            return "Medium"
        else:
            return "High"

    heatmap_df["Risk"] = heatmap_df["Cases"].apply(classify_risk)

    # Create map
    fig = px.choropleth(
        heatmap_df,
        locations="Country",
        locationmode="country names",
        color="Risk",
        hover_name="Country",
        color_discrete_map={
            "Low": "green",
            "Medium": "yellow",
            "High": "red"
        },
        title="🌍 Global Epidemic Risk Map"
    )

    return fig