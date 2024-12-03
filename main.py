import datetime
import random
import re
import time
from typing import List, Dict
from LouiesBurner.sports import SPORTS, Sport
from LouiesBurner.x import client


def create_tweet_text(highs: List[Dict]) -> str:
    """Create an engaging tweet about season high achievement(s)."""
    # If multiple achievements by same player, combine them
    player = highs[0]["Player"]
    if all(h["Player"] == player for h in highs):
        if len(highs) == 1:
            high = highs[0]
            single_templates = [
                "🚨 SEASON HIGH ALERT! 🚨\n{player} just {verb} {stat_type} with {value} against {opponent}! #AnchorUp ⚓️",
                "🔥 {player} is ON FIRE! 🔥\nJust set a season high with {value} {stat_type} vs {opponent}! #GLVCbsb",
                "⚡️ RECORD BREAKER ⚡️\n{player} leads the way with {value} {stat_type} against {opponent}! #AnchorUp",
                "👀 Look what {player} just did!\nNew season high: {value} {stat_type} vs {opponent}! #GLVCbsb ⚓️",
                "💪 BEAST MODE: {player} 💪\nDominates with {value} {stat_type} against {opponent}! #AnchorUp",
            ]

            # Determine appropriate verb
            stat = high["Statistic"].lower()
            if stat in ["strikeouts", "hits", "runs scored", "rbis"]:
                verb = "racked up"
            elif stat in ["home runs", "doubles", "triples"]:
                verb = "crushed"
            elif stat in ["stolen bases"]:
                verb = "swiped"
            elif stat in ["innings pitched"]:
                verb = "dominated for"
            else:
                verb = "recorded"

            return random.choice(single_templates).format(
                player=high["Player"],
                value=high["Value"],
                stat_type=stat,
                opponent=re.sub(r"\s*\([^)]*\)", "", high["Opponent"]),
                verb=verb,
            )
        else:
            # Combine multiple achievements
            achievements = []
            for high in highs:
                stat = high["Statistic"].lower()
                achievements.append(f"{high['Value']} {stat}")
            achievements_str = ", ".join(achievements[:-1]) + f" and {achievements[-1]}"
            multi_templates = [
                "🔥 WHAT A GAME! 🔥\n{player} sets multiple season highs with {achievements} against {opponent}! #AnchorUp ⚓️",
                "⚡️ {player} IS UNSTOPPABLE! ⚡️\nNew season highs: {achievements} vs {opponent}! #GLVCbsb",
                "💪 DOMINANT PERFORMANCE 💪\n{player} sets new highs with {achievements} against {opponent}! #AnchorUp",
            ]
            return random.choice(multi_templates).format(
                player=player,
                achievements=achievements_str,
                opponent=re.sub(r"\s*\([^)]*\)", "", highs[0]["Opponent"]),
            )

    # If we somehow get here (shouldn't with current logic), use a simple template
    high = highs[0]
    return f"🎯 New season high! {high['Player']} recorded {high['Value']} {high['Statistic'].lower()} against {re.sub(r'\s*\([^)]*\)', '', high['Opponent'])}! #AnchorUp"


def main(sport: str, date: datetime.date) -> None:
    sport_class = SPORTS.get(sport, None)
    assert sport_class is not None, f"Invalid sport '{sport}'"
    assert isinstance(sport_class, type) and issubclass(sport_class, Sport)

    # Create an instance of the sport class
    sport_obj = sport_class(year=date.year)

    # Get season highs set on the previous day
    new_highs = sport_obj.get_season_highs_for_date(date)

    # Group achievements by player
    from itertools import groupby
    from operator import itemgetter

    # Sort by player for grouping
    new_highs.sort(key=lambda x: x["Player"])

    # Create and post tweets for grouped achievements
    if new_highs:
        print(
            f"\nPosting tweets for season highs from {(date - datetime.timedelta(days=1)).strftime('%Y-%m-%d')}:"
        )

        # Group by player
        for player, group in groupby(new_highs, key=lambda x: x["Player"]):
            achievements = list(group)
            tweet_text = create_tweet_text(achievements)
            print(f"\nTweeting:\n{tweet_text}")
            try:
                client.create_tweet(text=tweet_text)
                print("Tweet posted successfully!")
                # Wait 1 minute between tweets to avoid rate limits
                time.sleep(60)
            except Exception as e:
                print(f"Error posting tweet: {e}")
                # If we hit rate limit, wait longer
                if "429" in str(e):
                    print("Rate limit hit, waiting 15 minutes...")
                    time.sleep(900)
    else:
        print(
            f"\nNo season highs were set on {(date - datetime.timedelta(days=1)).strftime('%Y-%m-%d')}"
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
