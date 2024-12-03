import datetime
import time
from itertools import groupby
from LouiesBurner.sports import SPORTS, Sport
from LouiesBurner.x import client


def main(
    sport: str, date: datetime.date, _retries: int = 5, _retry_sleep_time: int = 2
) -> None:
    if not _retries:
        return print("maximum retries reached, try again")

    sport_class = SPORTS.get(sport, None)
    assert sport_class is not None, f"Invalid sport '{sport}'"
    assert issubclass(sport_class, Sport), f"Invalid sport '{sport}'"

    sport_obj = sport_class(year=date.year)
    new_highs = sport_obj.get_season_highs_for_date(date)
    prev_date = (date - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    if not new_highs:
        return print(f"No {sport} szn highs were set on {prev_date}")

    new_highs.sort(key=lambda x: x["Player"])
    tweets = []
    for _, group in groupby(new_highs, key=lambda x: x["Player"]):
        achievements = list(group)
        tweet_txt = sport_obj.create_tweet_text(achievements)
        tweets.append(tweet_txt)
        try:
            client.create_tweet(text=tweet_txt)
            print("Tweet posted successfully!")
            time.sleep(_retry_sleep_time)
        except Exception as e:
            print(f"Error posting tweet: {e}")
            print(f"sleeping for {_retry_sleep_time}s")
            time.sleep(_retry_sleep_time)
            main(sport=sport, date=date, _retry_sleep_time=_retry_sleep_time - 1)

    return print(f"New tweets created: {'\n\n'.join(tweets)}")


if __name__ == "__main__":
    from argparse import ArgumentParser

    arg_parser = ArgumentParser()

    arg_parser.add_argument(
        "-sport",
        type=str,
        choices=list(SPORTS.keys()),
        help="name of sport to scrape",
        default="baseball",
    )

    arg_parser.add_argument(
        "-date",
        type=datetime.date.fromisoformat,
        help="Date in ISO format (YYYY-MM-DD). Will check previous day for season highs",
        default=datetime.date.today().isoformat(),
    )

    # parse arguments, and unpack them into main function
    _ = main(**arg_parser.parse_args().__dict__)
