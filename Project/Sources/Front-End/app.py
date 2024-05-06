from flask import Flask, redirect
from dashapp.sentiment.dash import sentiment
from dashapp.stat.dash import stat
from dashapp.home.dash import home

app = Flask(__name__)

app_home = home(app)
app_stat = stat(app)
app_sentiment = sentiment(app)

@app.route('/')
def index():
    return redirect('/home')

# if __name__ == "__main__":
#     app.run()
    
if __name__ == "__main__":
    app.run(host="0.0.0.0",  debug=True)
