from dash import Dash, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dashapp.navigation.nav import get_navigation

stylesheets = ['/static/css/home.css', '/static/css/style.css', '/static/css/bootstrap.min.css']

def home(flask_app):
    app = Dash(server=flask_app, routes_pathname_prefix='/home/', external_stylesheets=stylesheets, title='DADS5001')
    app.layout = html.Div([get_navigation(),
        dbc.Container([
            html.Div([
                html.Header([
                    html.H1("Final Project Report: DADS5001"),
                    html.H2("YouTube Influencer Analysis in the Tourism Sector")
                ]),
                html.Section([
                    html.H3("Objective"),
                    html.P("""Our goal is to develop a tool that aids entrepreneurs of all sizes in selecting influencers who provide value within a constrained budget. 
                           This tool extends beyond traditional metrics like views and subscriber counts, incorporating diverse data to support more strategic decisions. 
                           We extract YouTube data, including channel details and specific video content from each influencer. Using large language models (LLMs), 
                           we classify video titles related to tourism, analyze sentiment in video comments, and present our insights through Dash, an advanced data visualization tool."""),
                    html.H3("Problem Statement"),
                    html.P("""Entrepreneurs looking to engage influencers for promotional video content in tourism often face the challenge of choosing the right influencer amidst a saturated market, 
                           especially within limited budget constraints. The decision-making process can be overwhelming without comprehensive data analysis tools that summarize 
                           and visualize influencer data to enhance decision-making efficiency."""),
                    html.H3("Data Collection"),
                    html.P("""We employ Python scripts in Jupyter Notebook for data collection and transformation tasks. Data is fetched using the requests library to execute REST API calls to the YouTube API. 
                           The data is temporarily stored in pandas DataFrames for processing and subsequently exported to CSV files for persistence."""),
                    html.H3("Data Storage"),
                    html.P("Data is stored in CSV files."),
                    html.H3("Results of Data Analysis and Data Presentation"),
                    html.P("""Our analysis results are presented through two Dash-based dashboards:"""),
                    html.Ul([
                        html.Li("1.YouTuber's Channel Stats Analysis Dashboard", style={'font-weight': 'bold'}),
                        html.P("""This dashboard displays statistics for each YouTuber’s channel, such as total subscribers, views, published videos, and engagement metrics (likes and views). 
                               It evaluates the success of past influencer campaigns and examines the frequency of video uploads to assess how regularly influencers engage their audience."""),
                        html.Li("2.Video Comment Sentiment Analysis Dashboard", style={'font-weight': 'bold'}),
                        html.P("""Post-influencer engagement, this dashboard provides insights into the public reception of promotional videos. 
                               It analyzes sentiments expressed in video comments to determine if the promotion was received positively or negatively. 
                               For negative feedback, the dashboard highlights the most critical comments, enabling quick identification of issues for prompt resolution. 
                               This feature aids entrepreneurs in engaging with their audience effectively by addressing concerns and ensuring continuous improvement in customer satisfaction."""),
                    ]),
                    html.H3("Idea of using LLM models (Hugging Face)"),
                    html.Div([
                        html.Span("1. Facebook/bart-large-mnli", style={'font-weight': 'bold', 'margin-right': '10px'}),
                        html.A("Link", 
                            href="https://huggingface.co/facebook/bart-large-mnli",
                            target="_blank",
                            style={'color': '#007bff', 'text-decoration': 'none'}),
                    ], style={'display': 'flex', 'align-items': 'center', 'margin-bottom': '5px'}),
                    html.P("Task: Text classification", style={'margin-bottom': '5px'}),
                    html.P("""Application: We use this model to classify video titles as related or unrelated to tourism. This classification helps identify relevant video content for further analysis 
                           in the tourism sector and filters out non-tourism content for our YouTuber's Channel Stats Analysis Dashboard."""),
                    html.Div([
                        html.Span("2. Helsinki-NLP/opus-mt-th-en", style={'font-weight': 'bold', 'margin-right': '10px'}),
                        html.A("Link", 
                            href="https://huggingface.co/Helsinki-NLP/opus-mt-th-en",
                            target="_blank",
                            style={'color': '#007bff', 'text-decoration': 'none'}),
                    ], style={'display': 'flex', 'align-items': 'center', 'margin-bottom': '5px'}),
                    html.P("Task: Language translation (Thai to English)", style={'margin-bottom': '5px'}),
                    html.P("""Application: Many video titles in our dataset are in Thai, which is incompatible with the Facebook/bart-large-mnli model designed for English text. 
                           Therefore, we translate these titles from Thai to English prior to classification, ensuring accurate processing and analysis."""),
                    html.Div([
                        html.Span("3. Cardiffnlp/twitter-xlm-roberta-base-sentiment", style={'font-weight': 'bold', 'margin-right': '10px'}),
                        html.A("Link", 
                            href="https://huggingface.co/cardiffnlp/twitter-xlm-roberta-base-sentiment",
                            target="_blank",
                            style={'color': '#007bff', 'text-decoration': 'none'}),
                    ], style={'display': 'flex', 'align-items': 'center', 'margin-bottom': '5px'}),
                    html.P("Task: Sentiment analysis", style={'margin-bottom': '5px'}),
                    html.P("""Application: This model evaluates the sentiment of user comments on YouTube videos, categorizing them as positive, neutral, or negative, along with a confidence score. 
                           The results are crucial for our Video Comment Sentiment Analysis Dashboard, where they help visualize and analyze public sentiment towards promotional content, facilitating rapid response strategies to feedback."""),
                ], className="project-info"),
                html.Footer([
                    html.P("Project members: 6610422007 : Chayaphon Sornthananon | 6610422013 : Bunrawat Charoenyuennan"),
                    html.P("Subject: DADS5001 Data Analytics and Data Science Tools and Programming | Semester: 02/2023 | Submission: 11/05/2024"),
                    html.P("Lecturer: Asst. Prof. Dr. Ekarat Rattagan"),
                    html.P([
                        "Project Source Code: ",
                        html.A("Github", 
                            href="https://github.com/chayaphon/DADS5001/tree/main/Project",
                            target="_blank",
                            style={'color': '#007bff', 'text-decoration': 'none'})
                    ])
                ])
            ], style={'width': '100%', 'margin': '0 auto', 'padding': '20px', 'background': 'white', 'boxShadow': '0 0 10px rgba(0, 0, 0, 0.1)'})
        ])
    ])
    
    @app.callback(
        [Output('nav-home', 'className'),
        Output('nav-stat', 'className'),
        Output('nav-sentiment', 'className')],
        [Input('url', 'pathname')]
    )
    def update_nav_active(pathname):
        if not pathname:
            return ['nav-link'] * 3  # Default class for all if no pathname
        return [
            'nav-link active' if pathname == '/home/' else 'nav-link',
            'nav-link active' if pathname == '/stat/' else 'nav-link',
            'nav-link active' if pathname == '/sentiment/' else 'nav-link']
    
    return app
