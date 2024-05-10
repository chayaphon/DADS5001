import dash
from dash import html, dcc, Output, Input, State, dash_table
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dashapp.sentiment.function import *
import datetime
from dashapp.navigation.nav import get_navigation

stylesheets = ['/static/css/style.css', '/static/css/bootstrap.min.css']

def sentiment(flask_app):
    app = dash.Dash(server=flask_app, routes_pathname_prefix='/sentiment/', external_stylesheets=stylesheets, title='DADS5001')
    app.layout = create_layout()
    register_callbacks(app)
    return app

#-----------------------------------------------------------------------------------#
### Layout ###
#-----------------------------------------------------------------------------------#
def create_layout():
    return html.Div([
        get_navigation(),
        dbc.Container([
            dbc.Row([
                dbc.Col(
                    html.Div([
                        input_group(),
                        video_details(),
                        thumbnail_display()
                    ], style={"fontSize": "17px"}),
                    md=5, 
                    style={"marginLeft": "20px", "marginRight": "20px"}
                ),
                dbc.Col(
                    html.Div([
                        sentiment_header(),
                        sentiment_analysis_display()
                    ]),
                    md=6,
                    style={"marginLeft": "20px", "marginRight": "20px"}
                ),
            ]),
        ], fluid=True, style={"marginTop": "30px"})
    ])

def input_group():
    return dbc.InputGroup([
        dbc.Input(id='url-input', type='text', placeholder="Enter YouTube video URL", style={"marginRight": "10px"}),
        dbc.Button("Check", id='submit-button', n_clicks=0),
        dcc.Store(id='intermediate-data'),
    ], className="mb-3")

def video_details():
    return html.Div([
        html.H5("Video Title:", className="mt-3"),
        html.P(id='video-title'),
        html.H5("Channel Name:"),
        html.P(id='channel-name'),
        html.H5("Publish at:"),
        html.P(id='publish-at'),
        html.H5("Duration:"),
        html.P(id='duration'),
        html.H5("View:"),
        html.P(id='view'),
        html.H5("Like:"),
        html.P(id='like'),
        html.H5("Comment:"),
        html.P(id='comment')
    ])

def thumbnail_display():
    return html.Div([
        html.Img(id='video-thumbnail', src="", style={'width': 'auto', 'height': 'auto'})
    ], style={'border': '1px solid #ddd', 'padding': '10px', 'margin-top': '20px'})

def sentiment_header():
    return html.Div([
        html.H5("Sentiment : (top 1,000 comments)"),
        dbc.Row([
            dbc.Col(dbc.Badge("Positive", color="success", className="ml-1", style={"color": "white"})),
            dbc.Col(dbc.Badge("Neutral", color="primary", className="ml-1", style={"color": "white"})),
            dbc.Col(dbc.Badge("Negative", color="danger", className="ml-1", style={"color": "white"}))
        ], className="mb-3")
    ])

def sentiment_analysis_display():
    return dcc.Loading(
        id="loading-sentiment-content",
        type="circle",
        children=[
            dbc.Row([
                dbc.Col(html.P(id="positive_percentage")),
                dbc.Col(html.P(id="neutral_percentage")),
                dbc.Col(html.P(id="negative_percentage"))
            ], className="mb-3", style={"marginTop": "10px", "marginBottom": "10px", "fontSize": "18px", "fontWeight": "bold"}),
            html.Hr(style={"marginTop": "10px", "marginBottom": "10px"}),
            dcc.Graph(id='sentiment-bar-chart'),
            html.Div([
                html.H5("Sentiment Data"),
                html.Div(id='dash_table')
            ], style={'width': '100%'})
        ]
    )

#-----------------------------------------------------------------------------------#
### Callback ###
#-----------------------------------------------------------------------------------#

def register_callbacks(app):
    
    ###### Update Nav bar ######
    #----------------------------------------------------------------------#
    @app.callback(
        [Output('nav-home', 'className'),
        Output('nav-stat', 'className'),
        Output('nav-sentiment', 'className')],
        [Input('url', 'pathname')]
    )
    def update_nav_active(pathname):
        if not pathname:
            return ['nav-link'] * 3
        return [
            'nav-link active' if pathname == '/home/' else 'nav-link',
            'nav-link active' if pathname == '/stat/' else 'nav-link',
            'nav-link active' if pathname == '/sentiment/' else 'nav-link']
    #----------------------------------------------------------------------#


    ###### Update Info Data ######
    #----------------------------------------------------------------------#
    @app.callback(
        [
            Output('video-title', 'children'),
            Output('channel-name', 'children'),
            Output('publish-at', 'children'),
            Output('duration', 'children'),
            Output('view', 'children'),
            Output('like', 'children'),
            Output('comment', 'children'),
            Output('video-thumbnail', 'src'),
            Output('intermediate-data', 'data'),
        ],
        [
            Input('submit-button', 'n_clicks'),
        ],
        [State('url-input', 'value')]
    )
    def update_info(n_clicks, url):
        if not url or n_clicks == 0:
            raise PreventUpdate
        
        video_id = get_youtube_video_id(url)
        status_code, data = fetch_video_details(video_id)
        
        if status_code != 200:
            return ("No data available",) * 7, None, None
        
        df_info = pd.json_normalize(data['items'])
        df_info = df_info[info_cols]
        view_formatted = format(int(df_info['statistics.viewCount'].iloc[0]), ',')
        like_formatted = format(int(df_info['statistics.likeCount'].iloc[0]), ',')
        comment_formatted = format(int(df_info['statistics.commentCount'].iloc[0]), ',')
        published_at = datetime.datetime.fromisoformat(df_info['snippet.publishedAt'].iloc[0].replace('Z', '+00:00'))
        published_at_formatted = published_at.strftime('%B %d, %Y at %I:%M %p') + ' UTC'
        return (
            df_info['snippet.title'].iloc[0],
            df_info['snippet.channelTitle'].iloc[0],
            published_at_formatted,
            format_duration(df_info['contentDetails.duration'].iloc[0]),
            view_formatted,
            like_formatted,
            comment_formatted,
            df_info['snippet.thumbnails.high.url'].iloc[0],
            video_id,
        )
    #----------------------------------------------------------------------#
        

    ###### Update Sentiment Data ######
    #----------------------------------------------------------------------#
    @app.callback(
        [
            Output('positive_percentage', 'children'),
            Output('neutral_percentage', 'children'),
            Output('negative_percentage', 'children'),
            Output('sentiment-bar-chart', 'figure'),   
            Output('dash_table', 'children')
        ],
        Input('intermediate-data', 'data')
    )
    def update_sentiment(video_id):
        if video_id is None:
            raise PreventUpdate
        df_comment =  fetch_all_comments(video_id)
        sentiment_type = []
        sentiment_score = []
        df_comment = df_comment.rename(columns={'snippet.topLevelComment.snippet.textDisplay':'comment'})
        for comment in df_comment['comment']:
            comment = clean_comment(comment)
            comment = trim_comment(comment)
            result = sentiment_check(comment)
            sentiment_type.append(result[0]['label'])
            sentiment_score.append(round(result[0]['score'], 4))
        df_comment['sentiment_type'] = sentiment_type
        df_comment['sentiment_score'] = sentiment_score
        df_comment = df_comment[['comment','sentiment_type','sentiment_score']]
        SentimentPercent = label_text(df_comment)
        bar_chart = get_bar_chart(df_comment)
        dataTable = get_table(df_comment)
        return SentimentPercent[0], SentimentPercent[1], SentimentPercent[2], bar_chart, dataTable
    
    #----------------------------------------------------------------------#
    
    return app

#-----------------------------------------------------------------------------------#
### Visualize ###
#-----------------------------------------------------------------------------------#

def label_text(df_comment):
    total_entries = df_comment['sentiment_type'].count()
    sentiment_counts = df_comment['sentiment_type'].value_counts()
    sentiment_percentages = (sentiment_counts / total_entries) * 100
    positive = f"{sentiment_percentages.get('positive', 0):.2f}%"
    neutral = f"{sentiment_percentages.get('neutral', 0):.2f}%"
    negative = f"{sentiment_percentages.get('negative', 0):.2f}%"
    return positive, neutral, negative
    
def get_bar_chart(df_comment):
    sentiment_counts = df_comment['sentiment_type'].value_counts()
    sentiment_df = sentiment_counts.reset_index()
    fig = px.bar(
            sentiment_df,
            x='sentiment_type',
            y='count',
            title="Sentiment Counts",
            category_orders={'sentiment_type': ['positive', 'neutral', 'negative']},
            color='sentiment_type',
            color_discrete_map={'positive': '#4daf4a', 'neutral': '#377eb8', 'negative': '#e41a1c'},
            labels={'sentiment_type': 'Sentiment Type', 'count': 'Count'},
        )
    fig.update_traces(texttemplate='%{y}', textposition='outside')
    fig.update_layout(margin=dict(t=50), yaxis=dict(range=[0, sentiment_df['count'].max() * 1.1]))
    return fig

def get_table(df_comment):
    data = df_comment.to_dict('records')
    columns = [
        {"name": "Comment", "id": "comment"},
        {"name": "Sentiment", "id": "sentiment_type"},
        {"name": "Sentiment Score", "id": "sentiment_score", "type": "numeric", "format": dash_table.Format.Format(precision=4, scheme=dash_table.Format.Scheme.decimal)}
    ]
    Table = dash_table.DataTable(
            columns=columns,
            data=data,
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            style_table={'height': '400px', 'overflowY': 'auto'},
            style_cell={'textAlign': 'left'},
            style_header={
                'backgroundColor': 'white',
                'fontWeight': 'bold'
            },
            style_cell_conditional=[
                {'if': {'column_id': 'comment'}, 'width': '27vw', 'minWidth': '27vw', 'maxWidth': '27vw', 'overflow': 'hidden', 'textOverflow': 'ellipsis'},
                {'if': {'column_id': 'sentiment_type'}, 'width': '6vw', 'minWidth': '6vw', 'maxWidth': '6vw', 'overflow': 'hidden', 'textOverflow': 'ellipsis'},
                {'if': {'column_id': 'sentiment_score'}, 'width': '6vw', 'minWidth': '6vw', 'maxWidth': '6vw', 'overflow': 'hidden', 'textOverflow': 'ellipsis'}
            ],
            style_data_conditional=[
                {'if': {'column_id': 'sentiment_type', 'filter_query': '{sentiment_type} = "positive"'},
                'backgroundColor': '#d4edda', 'color': 'black'},
                {'if': {'column_id': 'sentiment_type', 'filter_query': '{sentiment_type} = "neutral"'},
                'backgroundColor': '#B9E4F8', 'color': 'black'},
                {'if': {'column_id': 'sentiment_type', 'filter_query': '{sentiment_type} = "negative"'},
                'backgroundColor': '#f8d7da', 'color': 'black'}
            ]
        )
    return Table
