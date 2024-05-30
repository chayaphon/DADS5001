import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd


# Sample data
data = {
    "Category": ["A", "B", "C", "D"],
    "Values": [4, 1, 2, 7]
}
df = pd.DataFrame(data)

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# App layout
app.layout = dbc.Container([
    dbc.Row([
        html.H1("Sameple Dashboard"),
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
            id='category-dropdown1',
            options=[{'label': cat, 'value': cat} for cat in df['Category']],
            value=['A'],
            multi=True,
            ),
        ])
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='bar-chart')
        ],)
        
    ],),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='ek-line-chart')
        ],)
        
    ],)
], fluid=True)

# Callback to update bar chart based on dropdown selection
@app.callback(
    [Output('bar-chart', 'figure'),Output('ek-line-chart', 'figure')],
    [Input('category-dropdown1', 'value')]
)
def update_bar_chart(selected_category):
    filtered_df = df[df['Category'].isin(selected_category)]
    fig = px.bar(filtered_df, 
                 x='Category',
                 y='Values',
                 title=f'Values for Category {selected_category}')
    
    fig_line = px.line(filtered_df, x='Category',
                   y='Values', title=f'Values for Category {selected_category}',
                   width=800,  # Set the width of the line chart
                   height=600)
    
    return fig , fig_line

# Run the app
if __name__ == '__main__':
    app.run_server(host='127.0.0.1', debug=True)
