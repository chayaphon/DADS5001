from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import base64, io
import pandas as pd
import numpy as np
from dashapp.navigation.nav import get_navigation

stylesheets = ['/static/css/style.css', '/static/css/bootstrap.min.css']

#-----------------------------------------------------------------------------------#
### Slicer ###
#-----------------------------------------------------------------------------------#

upload_button = dcc.Upload(
        id='upload-data',
        children=html.Button('Browse'),
        multiple=False,
        className='button'
    )
slicer_channel = dcc.Dropdown(
                id='channel-slicer',
                multi=True,
                className='dropdown'
            )
slicer_tourism_flag = dcc.Dropdown(
                id='tourism-slicer',
                value='Yes',
                multi=False,
                clearable=False,
                className='dropdown'
            )
slicer_view = dcc.RadioItems(
                id='viewType-slicer',
                options=[
                    {'label': 'Subscribe', 'value': 'sub'},
                    {'label': 'View', 'value': 'view'}
                ],
                value='sub',
                className='radio-items',
                labelStyle={'display': 'inline-block', 'marginRight': '20px'}
            )
slicer_year = dcc.RangeSlider(
                id='year-range-slider',
                step=1  
            )

#-----------------------------------------------------------------------------------#
### Layout ###
#-----------------------------------------------------------------------------------#
layout = html.Div([
        get_navigation(),
        html.Div([
            html.Label('Upload Data :', className='label'),
            upload_button,
            html.A("[download test data]", 
                href="https://raw.githack.com/chayaphon/DADS5001/main/Project/Sources/Data/test_data.csv",
                download="test_data.csv",
                target="_blank",
                style={'color': '#007bff', 'text-decoration': 'none'}, className='link'),
            dcc.Store(id='data-store'),
            html.Label('View By:', className='label'),
            slicer_view,
            html.Label('Tourism:', className='label'),
            slicer_tourism_flag,
            html.Label('Channel:', className='label'),
            slicer_channel,
        ], className='control-group'),
        html.Div([
            slicer_year
        ], style={'padding': '20px', 'width': '100vh'}),
        html.Div([ 
            dbc.Col(dcc.Graph(id='pie-chart'),width=6, style={'flex': '0 0 45%','margin-right': '8vh'}),
            dbc.Col(dcc.Graph(id='bar-chart'),width=6, style={'flex': '0 0 45%','margin-right': '5vh'}),
        ], style={'display': 'flex', 'justifyContent': 'space-around', 'width': '100%'}),
        html.Div([ 
            dbc.Col(dcc.Graph(id='line-chart'),width=6, style={'flex': '0 0 45%', 'margin-right': '8vh'}),
            dbc.Col(dcc.Graph(id='content-count-chart'),width=6, style={'flex': '0 0 45%', 'margin-right': '5vh'}),
        ], style={'display': 'flex', 'justifyContent': 'space-around', 'width': '100%'})
    ])

#-----------------------------------------------------------------------------------#
### Start App ###
#-----------------------------------------------------------------------------------#
def stat(flask_app):
    app = Dash(server=flask_app, routes_pathname_prefix='/stat/', external_stylesheets=stylesheets, title='DADS5001')
    app.layout = layout

    ### navbar active update ###
    @app.callback(
        [
            Output('nav-home', 'className'),
            Output('nav-stat', 'className'),
            Output('nav-sentiment', 'className')
        ],
        [
            Input('url', 'pathname')
        ]
    )
    def update_nav_active(pathname):
        if not pathname:
            return ['nav-link'] * 3
        return [
            'nav-link active' if pathname == '/home/' else 'nav-link',
            'nav-link active' if pathname == '/stat/' else 'nav-link',
            'nav-link active' if pathname == '/sentiment/' else 'nav-link']
        
    ### Upload Data
    @app.callback(
        [
            Output('data-store', 'data'),
            Output('channel-slicer', 'options'),
            Output('channel-slicer', 'value'),
            Output('tourism-slicer', 'options'),
            Output('year-range-slider', 'min'),
            Output('year-range-slider', 'max'),
            Output('year-range-slider', 'value'),
            Output('year-range-slider', 'marks'),
        ],
    Input('upload-data', 'contents'),
    prevent_initial_call=True
    )
    def update_output(list_of_contents):
        if list_of_contents is not None:
            content_type, content_string = list_of_contents.split(',')
            decoded = base64.b64decode(content_string)
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            df = df[['channel_name','tourism_flag','publishedAt','subscriber_count','views']]
            df['publishedAt'] = pd.to_datetime(df['publishedAt'])
            channel_name = df['channel_name'].unique()
            tourism_flag = df['tourism_flag'].unique()
            tourism_flag = np.append(tourism_flag, 'All')
            min_year = min(df['publishedAt']).year
            max_year = max(df['publishedAt']).year
            return [
                df.to_dict('records'),
                channel_name,
                channel_name,
                tourism_flag,
                min_year,
                max_year,
                [max_year-1, max_year],
                {year: str(year) for year in range(min_year, max_year+1)}]

    ### visual update ###
    @app.callback(
        [
            Output('pie-chart', 'figure'),
            Output('bar-chart', 'figure'),
            Output('line-chart', 'figure'),
            Output('content-count-chart', 'figure')
        ],
        [
            Input('viewType-slicer', 'value'),   
            Input('tourism-slicer', 'value'),
            Input('channel-slicer', 'value'),
            Input('year-range-slider', 'value'),
            Input('data-store', 'data'),
        ],
        prevent_initial_call=True
    )
    
    def update_charts(viewType, tourism_flag, channels, year_range, data):
        df = pd.DataFrame(data)
        df['publishedAt'] = pd.to_datetime(df['publishedAt'])
        colors = px.colors.qualitative.Set1
        color_map = {channel: color for channel, color in zip(df['channel_name'].unique(), colors)}
        
        if tourism_flag == 'All':
            tourism_flag = ["Yes","No"]
        else:
            tourism_flag = [tourism_flag]
        
        filtered_df = df[(df['channel_name'].isin(channels)) & 
                        (df['tourism_flag'].isin(tourism_flag)) &
                        (df['publishedAt'].dt.year >= year_range[0]) &
                        (df['publishedAt'].dt.year <= year_range[1])]
        
        # Aggr for top2 chart
        if viewType == 'sub':
            aggregated_data = filtered_df.groupby('channel_name')['subscriber_count'].max().reset_index()
            values = 'subscriber_count'
        else:
            aggregated_data = filtered_df.groupby('channel_name')['views'].sum().reset_index()
            values = 'views'
            
        out1 = get_pie_chart(aggregated_data, values, viewType, color_map)
        out2 = get_bar_chart(aggregated_data, values, viewType, color_map)
        out3 = get_line_chart(filtered_df, color_map)
        out4 = get_bar_chart_content(filtered_df, color_map)
        return out1, out2, out3, out4

    return app

#-----------------------------------------------------------------------------------#
### Visualization ###
#-----------------------------------------------------------------------------------#

#------------------------Pie Chart---------------------------#
def get_pie_chart(data, values, viewType, color_map):
    title_text = 'Current Subscriber by Channel' if viewType == 'sub' else 'Total Views by Channel'
    fig = px.pie(
            data, 
            values=values, 
            names='channel_name', 
            title=title_text,
            color='channel_name',
            color_discrete_map=color_map,
            hole=0.3,
            )
    fig.update_traces(
            #textinfo='label+percent+value',
            textinfo='label+percent',
            textposition='auto',
            hovertemplate='%{label}<br>%{value}<br>%{percent}',
            )
    fig.update_layout(
        legend_title_text='Channel'
    )
    return fig

#------------------------Bar Chart---------------------------#
def get_bar_chart(data, values, viewType, color_map):
    title_text = 'Current Subscriber by Channel' if viewType == 'sub' else 'Total Views by Channel'
    fig = px.bar(
        data,
        x=values, 
        y='channel_name',
        title=title_text,
        orientation='h',
        color='channel_name',
        color_discrete_map=color_map,
        text=values,
        labels={'channel_name': 'Channel'},
    )
    fig.update_traces(
        texttemplate='%{x:.2s}',
        textposition='auto',
        hovertemplate='<b>Channel:</b> %{y}<br><b>Views:</b> %{x}<extra></extra>'
        )
    fig.update_layout(
        xaxis_title="Count",
        yaxis_title="Channel",
        title=title_text
    )

    return fig

#------------------------Line Chart---------------------------
def get_line_chart(data, color_map):
    data['month_year'] = data['publishedAt'].dt.to_period('M').dt.to_timestamp()
    grouped_df = data.groupby(['month_year', 'channel_name']).agg({'views': 'sum'}).reset_index()

    fig = px.line(
        grouped_df,
        x='month_year',
        y='views',
        color='channel_name',
        color_discrete_map=color_map,
        title='Total Views by Month and Year',
        labels={'month_year': 'Month-Year', 'views': 'Total Views', 'channel_name': 'Channel'},
        #text='views'
    )
    fig.update_traces(
        #texttemplate='%{text:.3s}',
        #textposition='top center', 
        #mode='lines+markers+text',
        mode='lines+markers',
        # textfont=dict(
        #     family="Arial",
        #     size=12,
        #     color="black"
        # )
    )
    fig.update_xaxes(
        dtick="M1",
        tickformat="%b %Y",
        ticklabelmode="period"
    )
    fig.update_layout(
        xaxis_title='Period',
        yaxis_title='Total Views')

    return fig

#------------------------Bar Chart Content Count ---------------------------
def get_bar_chart_content(data, color_map):
    data['month_year'] = data['publishedAt'].dt.to_period('M').dt.to_timestamp()
    grouped = data.groupby(['month_year', 'channel_name']).size().reset_index(name='count')

    fig = px.bar(
        grouped, 
        x='month_year', 
        y='count', 
        color='channel_name', 
        color_discrete_map=color_map,
        barmode='group',
        labels={'count': 'Total Content', 'month_year': 'Period', 'channel_name': 'Channel'}
    )
    fig.update_xaxes(
        dtick="M1",
        tickformat="%b %Y",
        ticklabelmode="period"
    )
    fig.update_layout(
        title_text='Number of content per month',
        xaxis_title='Period',
        yaxis_title='Total content'
    )

    return fig
