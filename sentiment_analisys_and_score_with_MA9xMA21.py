import yfinance as yf
import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import requests

# Ticker for Ethereum
ticker = 'ETH-USD'

# URL for Ethereum API
url = "https://min-api.cryptocompare.com/data/v2/news/?categories=ETH&lang=EN"

# Request data from API
response = requests.get(url)

# Parse JSON response
data = json.loads(response.text)
print(data)

# Initialize sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Initialize variables
sentiment_score = 0
num_articles = 0

# Loop through articles and calculate sentiment score
for article in data['Data']:
    title = article['title']
    text = article['body']
    sentiment = analyzer.polarity_scores(title + ' ' + text)['compound']
    sentiment_score += sentiment
    num_articles += 1
print(num_articles)

# Calculate average sentiment score
avg_sentiment_score = sentiment_score / num_articles

# Retrieve Ethereum price data
ethereum_data = yf.download(ticker, period='3y', interval='1d')
ethereum_data = ethereum_data[['Close']]
ethereum_data.columns = ['close']

# Calculate 9 and 21-day moving averages of Ethereum price
ma_short = 9
ma_long = 21
ethereum_data.loc[:, 'MA_short'] = ethereum_data['close'].rolling(window=ma_short).mean().values
ethereum_data.loc[:, 'MA_long'] = ethereum_data['close'].rolling(window=ma_long).mean().values

# Check for 9-day moving average crossing above 21-day moving average
if ethereum_data.iloc[-2]['MA_short'] < ethereum_data.iloc[-2]['MA_long'] and ethereum_data.iloc[-1]['MA_short'] > ethereum_data.iloc[-1]['MA_long']:
    print('9-day MA has crossed above 21-day MA')

# Check for 9-day moving average crossing below 21-day moving average
if ethereum_data.iloc[-2]['MA_short'] > ethereum_data.iloc[-2]['MA_long'] and ethereum_data.iloc[-1]['MA_short'] < ethereum_data.iloc[-1]['MA_long']:
    print('9-day MA has crossed below 21-day MA')
print(ethereum_data)

# Retrieve current Ethereum price
current_price = ethereum_data.iloc[-1]['close']

# Calculate score based on sentiment, moving average price, and moving average crossover
if ethereum_data.iloc[-1]['MA_short'] > ethereum_data.iloc[-1]['MA_long']:
    score = (avg_sentiment_score * 100) + (current_price / ethereum_data.iloc[-ma_short]['MA_short']) + 20
    print(0)
elif ethereum_data.iloc[-1]['MA_short'] < ethereum_data.iloc[-1]['MA_long']:
    score = (avg_sentiment_score * 100) + (current_price / ethereum_data.iloc[-ma_short]['MA_short']) - 20
    print(1)
else:
    score = (avg_sentiment_score * 100) + (current_price / ethereum_data.iloc[-ma_short]['MA_short'])
    print(2)

# Define thresholds for "bad," "regular," and "good" scores
print(avg_sentiment_score)
print("bad = 0 <= n < 50","regular = 50 <= n < 70","good = n >= 70")
print("n = ",score)

