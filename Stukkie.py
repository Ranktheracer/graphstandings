import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Load live data from Google Sheets
sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR2hITWj8waraEYGbH-iYCfiCkUXxUlKtRuQYrmAwAfk07bCh60ghIS4nzgZuQLxWbYzbxVaYr4MBYt/pub?output=csv&gid=637972155"

df = pd.read_csv(sheet_url)

# Rename the column to standardize it (optional but cleaner)
df.rename(columns={"Race": "Race"}, inplace=True)

# Ensure Race is treated in its original order
df["Race"] = pd.Categorical(df["Race"], categories=df["Race"].astype(str).unique(), ordered=True)
df = df.sort_values("Race")

# Transform the data to long format
df = df.melt(id_vars=["Race"], var_name="Naam", value_name="Score")

# Create Dash app
app = dash.Dash(__name__)
app.title = "F1 Voorspellingen 2024"
server = app.server

# Layout of the app
app.layout = html.Div([
    html.H1("Standings F1-predictions 2024"),
    dcc.Checklist(
        id='naam-filter',
        options=[{'label': naam, 'value': naam} for naam in df['Naam'].unique()],
        value=df['Naam'].unique().tolist(),
        inline=True
    ),
    dcc.Graph(id='lijn-grafiek')
])

# Update the graph based on selected names
@app.callback(
    Output('lijn-grafiek', 'figure'),
    Input('naam-filter', 'value')
)
def update_graph(geselecteerde_namen):
    gefilterde_df = df[df['Naam'].isin(geselecteerde_namen)]
    fig = {
        'data': [
            {
                'x': gefilterde_df[gefilterde_df['Naam'] == naam]['Race'],
                'y': gefilterde_df[gefilterde_df['Naam'] == naam]['Score'],
                'type': 'line',
                'name': naam
            }
            for naam in geselecteerde_namen
        ],
        'layout': {
            'title': 'Scores per race',
            'xaxis': {'title': 'Race'},
            'yaxis': {'title': 'Score', 'range': [20, 70]},
        }
    }
    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
