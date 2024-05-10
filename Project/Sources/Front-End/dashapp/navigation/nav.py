from dash import html, dcc

def get_navigation():
    # The 'id' is important for accessing the pathname in callback
    location = dcc.Location(id='url', refresh=False)

    return html.Div([
        html.H1("YouTube Influencer Analysis in Tourism Sector", style={
            'textAlign': 'center',
            'backgroundColor': '#2C3E50',
            'color': 'white',
            'padding': '12px',
            'font-size': '36px',
            'marginTop': '0px',
            'marginBottom': '0px',
            'font-family': 'Arial, sans-serif'
        }),
        location,  # This component will capture and store the current URL
        html.Div([
            html.Nav([
                html.A('Home', href='/home/', id='nav-home', className='nav-link'),
                html.A('Channel Stats Analysis', href='/stat/', id='nav-stat', className='nav-link'),
                html.A('Comment Sentiment Analysis', href='/sentiment/', id='nav-sentiment', className='nav-link')
            ], style={
                'display': 'flex', 
                'justifyContent': 'center', 
                'alignItems': 'center',
            })
        ], className='nav-container')
    ], style={'textAlign': 'center', 'width': '100%'})
