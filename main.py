import datetime
import time
from itertools import groupby
from LouiesBurner.sports import SPORTS, Sport
from LouiesBurner.x import client


def main(sport: str, date: datetime.date) -> None:
    sport_class = SPORTS.get(sport, None)
    assert sport_class is not None, f"Invalid sport '{sport}'"
    assert isinstance(sport_class, type) and issubclass(sport_class, Sport)

    # Create an instance of the sport class
    sport_obj = sport_class(year=date.year)

    # Get season highs set on the previous day
    new_highs = sport_obj.get_season_highs_for_date(date)

    # Create and post tweets for grouped achievements
    if new_highs:
        print(
            f"Posting tweets for season highs from {(date - datetime.timedelta(days=1)).strftime('%Y-%m-%d')}:"
        )

        # Sort by player for grouping
        new_highs.sort(key=lambda x: x["Player"])

        # Group by player and create tweets
        for player, group in groupby(new_highs, key=lambda x: x["Player"]):
            achievements = list(group)
            tweet_text = sport_obj.create_tweet_text(achievements)
            print(f"\nTweeting:\n{tweet_text}")
            try:
                client.create_tweet(text=tweet_text)
                print("Tweet posted successfully!")
                time.sleep(2)  # watch rate limits
            except Exception as e:
                print(f"Error posting tweet: {e}")
                # If we hit rate limit, wait longer
                if "429" in str(e):
                    print("Rate limit hit, waiting 15 minutes...")
                    time.sleep(900)
    else:
        print(
            f"No {sport} season highs were set on {(date - datetime.timedelta(days=1)).strftime('%Y-%m-%d')}"
        )


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
