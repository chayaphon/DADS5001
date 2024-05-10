import pandas as pd
import requests
import re
from transformers import pipeline

api_key = ""

info_cols = ['snippet.channelTitle','snippet.title','snippet.publishedAt','snippet.thumbnails.high.url',
             'snippet.thumbnails.high.width','snippet.thumbnails.high.height','contentDetails.duration',
             'statistics.viewCount','statistics.likeCount','statistics.commentCount']
comment_cols = ['snippet.topLevelComment.snippet.authorDisplayName','snippet.topLevelComment.snippet.textDisplay','snippet.topLevelComment.snippet.likeCount','snippet.topLevelComment.snippet.updatedAt']

def fetch_video_details(video_id):
    url = "https://www.googleapis.com/youtube/v3/videos"
    params = {
        'part': 'snippet,statistics,contentDetails',
        'id': video_id,
        'key': api_key
    }
    response = requests.get(url, params=params)
    return response.status_code, response.json()

def fetch_all_comments(video_id):
    comments = []
    url = "https://www.googleapis.com/youtube/v3/commentThreads"
    params = {
        'part': 'snippet',
        'videoId': video_id,
        'key':  api_key,
        'maxResults': 100  # max retrieve 100 comments per request
    }
    while True:
        response = requests.get(url, params=params).json()
        comments.extend(response.get('items', []))
        # Check if there is a next page
        if 'nextPageToken' in response:
            params['pageToken'] = response['nextPageToken']
        else:
            break
    df = pd.json_normalize(comments)
    df = df[comment_cols]
    return df[:1000]

def sentiment_check(text):
    sentiment_analyzer = pipeline("sentiment-analysis", model="cardiffnlp/twitter-xlm-roberta-base-sentiment")
    results = sentiment_analyzer(text)
    return results

def format_duration(duration):
    pattern = re.compile(r'PT(\d+H)?(\d+M)?(\d+S)?')
    match = pattern.match(duration)
    hours, minutes, seconds = match.groups()
    hours = int(hours[:-1]) if hours else 0
    minutes = int(minutes[:-1]) if minutes else 0
    seconds = int(seconds[:-1]) if seconds else 0
    time_parts = []
    if hours:
        time_parts.append(f"{hours} hours" if hours > 1 else "1 hour")
    if minutes:
        time_parts.append(f"{minutes} minutes" if minutes > 1 else "1 minute")
    if seconds:
        time_parts.append(f"{seconds} seconds" if seconds > 1 else "1 second")
    return ', '.join(time_parts)

def clean_comment(raw_html):
    cleanr = re.compile('<.*?>')  # Regex to find HTML tags
    cleantext = re.sub(cleanr, '', raw_html)  # Replace HTML tags with ''
    normalized_text = re.sub(r'\s+', ' ', cleantext)
    return normalized_text.strip()

def trim_comment(text, max_length=1500):
    if len(text) > max_length:
        return text[:max_length]
    return text

def get_youtube_video_id(url):
    # Regex patterns to find the video ID in various YouTube URL formats
    patterns = [
        r"youtube\.com/watch\?v=([^\&\?\/]+)",  # Standard YouTube URL
        r"youtube\.com/embed/([^\&\?\/]+)",     # Embedded YouTube URL
        r"youtube\.com/shorts/([^\&\?\/]+)",    # YouTube Shorts URL
        r"youtu\.be/([^\&\?\/]+)",              # Shortened YouTube URL
        r"youtube\.com/live/([^\&\?\/]+)"       # Live YouTube URL
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None
