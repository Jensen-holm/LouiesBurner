import tweepy

CLIENT_SECRET = "cQtHR0N_t9SI1JlyLL8sUpJFHfUB_Asq63m1vktq2I5d-BCeHL"
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAF9gvwEAAAAAweoj8oKjujdFi1y%2Fs86fxJ9fPQ0%3DiCnUO8WwxdUYyCSyHoVrguVOlruZ0BUjkzD1K9wRX09wo7d8oz"
CONSUMER_KEY = "jzRjvlOWZk1WQpeXo6CFUtQGI"
CONSUMER_SECRET = "HXB97ql2ovXhCRAAVheadnu7IFGEKh2Y3v4olA2RR8yT6C6gYG"
ACCESS_TOKEN = "1834002975854870528-WrwD6PnHbRrl3t04r54RVLYNvIBaGi"
ACCESS_TOKEN_SECRET = "lnzkjnS7DlHkEOFVGLzyk9RtjrDHpUIhMVmzJN8yCN5OV"


_auth = tweepy.OAuth1UserHandler(
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET,
)

api = tweepy.API(_auth)

client = tweepy.Client(
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET,
)

