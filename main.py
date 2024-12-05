import datetime
import time
from itertools import groupby
from LouiesBurner.sports import SPORTS
from LouiesBurner.x import client


def main(
    sport: str,
    date: datetime.date,
    _retries: int = 5,
    _retry_sleep_time: int = 2,
) -> None:
    """
    Process and tweet season highs for a specified sport and date.

    Parameters
    ----------
    sport : str
        The name of the sport to process. Must be one of the keys in SPORTS dictionary.
    date : datetime.date
        The date to check for season highs. Will check the previous day's data.
    _retries : int, optional
        Number of retry attempts if tweet posting fails, by default 5.
    _retry_sleep_time : int, optional
        Time in seconds to sleep between retries, by default 2.

    Returns
    -------
    None
        Prints success/failure messages and posted tweets.

    Notes
    -----
    The function performs the following steps:
    1. Validates the sport and creates appropriate sport object
    2. Gets season highs for the specified date
    3. Groups achievements by player
    4. Creates and posts tweets for each player's achievements
    5. Handles posting failures with retries
    """
    if not _retries:
        return print("maximum retries reached, try again")

    sport_class = SPORTS.get(sport, None)
    assert sport_class is not None, f"Invalid sport '{sport}'"

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
        try:
            client.create_tweet(text=tweet_txt)
            print("Tweet posted successfully!")
            tweets.append(tweet_txt)
            time.sleep(_retry_sleep_time)
        except Exception as e:
            print(f"Error posting tweet: {e}")
            print(f"sleeping for {_retry_sleep_time}s")
            time.sleep(_retry_sleep_time)
            _ = main(
                sport=sport,
                date=date,
                _retry_sleep_time=_retry_sleep_time,
                _retries=_retries - 1,
            )

    return print(f"New tweets created:\n{'\n\n'.join(tweets)}")


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
