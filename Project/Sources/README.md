## Structure
Manually download data from the YouTube API by executing the notebook located at /Back-End/getdata.ipynb.
<br> Utilize /Back-End/llm.ipynb to classify video titles.

## Back-End Directory
- getdata.ipynb [link to code](https://github.com/chayaphon/DADS5001/tree/main/Project/Sources/Back-End/getdata.ipynb)
- llm.ipynb [link to code](https://github.com/chayaphon/DADS5001/tree/main/Project/Sources/Back-End/llm.ipynb)

### Workflow:
![Image](https://raw.githubusercontent.com/chayaphon/DADS5001/main/Project/be1.png)
![Image](https://raw.githubusercontent.com/chayaphon/DADS5001/main/Project/be2.png)

## Data
- data.csv
- data_clean.csv (use for Dash front-end in YouTuber's Channel Stats Analysis Dashboard)

## Front-End Directory
The front-end is powered by Flask which routes requests to various Dash apps. The YouTuber's Channel Stats Analysis Dashboard visualizes data from data_clean.csv provided by the back-end. 
The Video Comment Sentiment Analysis Dashboard fetches real-time video data, performs sentiment analysis, and visualizes the results.
- app.py
- dashapp/home/dash.py
- dashapp/navigation/nav.py
- dashapp/stat/dash.py (YouTuber's Channel Stats Analysis Dashboard)
- dashapp/sentiment/dash.py (Video Comment Sentiment Analysis Dashboard)
- dashapp/sentiment/function.py

## YouTuber's Channel Stats Analysis Dashboard
Upload data.csv obtained from the YouTube data download script in the back-end, and display it on this dashboard. 
![Image](https://raw.githubusercontent.com/chayaphon/DADS5001/main/Project/stat_dashboard1.png)
![Image](https://raw.githubusercontent.com/chayaphon/DADS5001/main/Project/stat_dashboard2.png)

## Video Comment Sentiment Analysis Dashboard
Enter a YouTube URL in this dashboard to fetch data, perform sentiment analysis using the llm model, and visualize the results.
![Image](https://raw.githubusercontent.com/chayaphon/DADS5001/main/Project/sentiment_dashboard.png)