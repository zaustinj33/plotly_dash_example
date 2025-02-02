import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Sample Data
df = pd.DataFrame({
    "Gene": ["GeneA", "GeneB", "GeneC", "GeneD", "GeneE"],
    "Enrichment_Sample1": [1.2, 2.3, 3.1, 0.5, 1.8],
    "Enrichment_Sample2": [2.1, 1.9, 2.8, 1.2, 3.0],
    "Q_Value": [0.05, 0.01, 0.02, 0.07, 0.03]
})

# Initialize Dash app
app = dash.Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1("Gene Enrichment Scatter Plot"),
    dcc.Graph(
        id="scatter-plot",
        config={"displayModeBar": False}  # Hide the mode bar for cleaner look
    )
])

# Callback to update scatter plot
@app.callback(
    Output("scatter-plot", "figure"),
    Input("scatter-plot", "id")  # Placeholder input, only need to load once
)
def update_scatter(_):
    fig = px.scatter(
        df,
        x="Enrichment_Sample1",
        y="Enrichment_Sample2",
        text="Gene",
        hover_data={"Gene": True, "Enrichment_Sample1": True, "Enrichment_Sample2": True, "Q_Value": True},
        labels={"Enrichment_Sample1": "Sample 1 Enrichment", "Enrichment_Sample2": "Sample 2 Enrichment"},
    )
    fig.update_traces(marker=dict(size=10, opacity=0.7))
    fig.update_layout(title="Interactive Gene Enrichment Scatter Plot")
    return fig

# Run app
if __name__ == "__main__":
    app.run_server(debug=True)
