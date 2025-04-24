# Gene Enrichment Visualization Dashboard

## Overview
This is an interactive web-based dashboard built with Dash and Plotly for visualizing gene enrichment data. The application allows researchers to explore relationships between gene enrichment values across different samples through an interactive scatter plot with additional analytical features.

## Features
- **Interactive Scatter Plot**: Visualize enrichment values between two samples with hover information
- **Axis Scaling Options**: Toggle between linear and logarithmic scales for both axes
- **Data Selection Tools**: Select points via lasso or box selection tools
- **Marginal Distributions**: View histogram (x-axis) and violin plot (y-axis) distributions
- **Gene Search**: Filter visualization by gene name
- **Dynamic Data Table**: View details of selected or visible genes with sorting and filtering capabilities

## Dependencies
- NumPy
- Pandas
- Plotly Express
- Dash
- Dash Core Components
- Dash HTML Components
- Dash Bootstrap Components
- Dash Table

## How It Works
1. The app simulates sample gene enrichment data (in a real application, this can be replaced with actual experimental data)
2. Users can interact with the scatter plot by:
   - Zooming in/out to focus on specific regions
   - Selecting points with lasso or box selection tools
   - Searching for specific genes
   - Changing axis scales between linear and logarithmic
3. The data table automatically updates to show:
   - Selected genes when using selection tools
   - Genes visible in the current view
   - Genes matching search criteria

## Usage
Run the application with:
```python
python app.py
```
Then navigate to http://127.0.0.1:8050/ in your web browser to access the dashboard.

## Potential Improvements
- Add more filtering options based on Q-values or other metrics
- Implement export functionality for selected data points
- Add statistical analysis features for selected gene subsets ( mean, std, 
- Integrate with real experimental data sources

