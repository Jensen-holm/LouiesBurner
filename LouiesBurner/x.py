from tweepy import API, Client, OAuth1UserHandler
import os

CLIENT_ID = os.environ.get("LOUIES_CLIENT_ID")
CLIENT_SECRET = os.environ.get("LOUIES_CLIENT_SECRET")
BEARER_TOKEN = os.environ.get("LOUIES_BEARER_TOKEN")
ACCESS_TOKEN = os.environ.get("LOUIES_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.environ.get("LOUIES_ACCESS_TOKEN_SECRET")
CONSUMER_KEY = os.environ.get("LOUIES_API_KEY")
CONSUMER_SECRET = os.environ.get("LOUIES_API_KEY_SECRET")


_auth = OAuth1UserHandler(
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET,
)

api = API(_auth)

client = Client(
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET,
)


if __name__ == "__main__":
    client.create_tweet(text="hello world!")
