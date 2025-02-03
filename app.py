import numpy as np
import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

import dash_table  # Import for DataTable

# Simulate Data: Binomial (X) & Normal (Y) Distribution
np.random.seed(42)
num_points = 1000
genes = [f"Gene_{i}" for i in range(num_points)]

# Generate binomial distribution and apply log transformation
x_values = np.random.normal(loc=10, scale=3, size=num_points)
y_values = np.random.normal(loc=10, scale=3, size=num_points)

# Generate q-values
q_values = np.random.uniform(0, 0.1, size=num_points)

df = pd.DataFrame({
    "Gene": genes,
    "Enrichment_Sample1": x_values,
    "Enrichment_Sample2": y_values,
    "Q_Value": q_values
})

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    html.H1("Gene Enrichment Scatter Plot", className="text-center mt-4"),

    # Axis Scaling Dropdowns
    dbc.Row([
        dbc.Col([
            html.Label("X-Axis Scale:"),
            dcc.Dropdown(
                id="x-scale",
                options=[{"label": "Linear", "value": "linear"},
                         {"label": "Log", "value": "log"}],
                value="linear", clearable=False
            )
        ], width=3),
        
        dbc.Col([
            html.Label("Y-Axis Scale:"),
            dcc.Dropdown(
                id="y-scale",
                options=[{"label": "Linear", "value": "linear"},
                         {"label": "Log", "value": "log"}],
                value="linear", clearable=False
            )
        ], width=3)
    ], className="mb-4"),

    # Scatter Plot
    dcc.Graph(id="scatter-plot", config={"modeBarButtonsToAdd": ["lasso2d", "select2d"]}),

    # Search Box
    html.Label("Search Gene:"),
    dcc.Input(id="search-input", type="text", placeholder="Enter gene name...", debounce=True),

    # Table for Selected or Visible Points
    html.H4("Visible Genes", className="mt-4"),
    dash_table.DataTable(
        id="selection-table",
        columns=[
            {"name": "Gene", "id": "Gene", "type": "text"},
            {"name": "Enrichment Sample 1", "id": "Enrichment_Sample1", "type": "numeric"},
            {"name": "Enrichment Sample 2", "id": "Enrichment_Sample2", "type": "numeric"},
            {"name": "Q Value", "id": "Q_Value", "type": "numeric"}
        ],
        page_size=20,
        style_table={"overflowX": "auto"},
        style_cell={"textAlign": "center"},
        style_header={"fontWeight": "bold"},
        sort_action="native",  # Enable sorting
        filter_action="native",  # Enable search filter
    )
], fluid=True)

# Callback to update scatter plot based on axis scaling
@app.callback(
    Output("scatter-plot", "figure"),
    [Input("x-scale", "value"),
     Input("y-scale", "value")]
)
def update_scatter(x_scale, y_scale):
    fig = px.scatter(
        df, x="Enrichment_Sample1", y="Enrichment_Sample2",
        hover_data={"Gene": True, "Enrichment_Sample1": True, "Enrichment_Sample2": True, "Q_Value": True},
        labels={"Enrichment_Sample1": "Sample 1 Enrichment (Log Transformed)", 
                "Enrichment_Sample2": "Sample 2 Enrichment"},
        marginal_x="histogram",  
        marginal_y="violin",  
    )

    for trace in fig.data:
        if trace.type == "scatter":  
            trace.marker.update(size=6, opacity=0.7)

    fig.update_layout(
        title="Interactive Gene Enrichment Scatter Plot",
        xaxis_type=x_scale, yaxis_type=y_scale
    )

    return fig

# Callback to update the table based on selection, viewport, or search
@app.callback(
    Output("selection-table", "data"),
    [Input("scatter-plot", "selectedData"),
     Input("scatter-plot", "relayoutData"),
     Input("search-input", "value")]
)
def update_table(selectedData, relayoutData, search_query):
    if selectedData and "points" in selectedData:
        selected_genes = [p["customdata"][0] for p in selectedData["points"]]
        filtered_df = df[df["Gene"].isin(selected_genes)]
    else:
        if relayoutData and "xaxis.range" in relayoutData:
            x_range = relayoutData["xaxis.range"]
        else:
            x_range = [df["Enrichment_Sample1"].min(), df["Enrichment_Sample1"].max()]

        if relayoutData and "yaxis.range" in relayoutData:
            y_range = relayoutData["yaxis.range"]
        else:
            y_range = [df["Enrichment_Sample2"].min(), df["Enrichment_Sample2"].max()]

        filtered_df = df[
            (df["Enrichment_Sample1"] >= x_range[0]) & (df["Enrichment_Sample1"] <= x_range[1]) &
            (df["Enrichment_Sample2"] >= y_range[0]) & (df["Enrichment_Sample2"] <= y_range[1])
        ]

    # Apply search filter if user types in search box
    if search_query:
        filtered_df = filtered_df[filtered_df["Gene"].str.contains(search_query, case=False, na=False)]

    return filtered_df.to_dict("records")

# Run app
if __name__ == "__main__":
    app.run_server(debug=True)
