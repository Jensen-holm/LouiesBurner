# from datetime import datetime

import requests
from bs4 import BeautifulSoup

from LouiesBurner.schedule import get_womens_soccer_schedule, find_most_recent_past_date
from LouiesBurner.scraping import get_game_data_by_date
from LouiesBurner.x import client

if __name__ == "__main__":
    html_soup_stats = BeautifulSoup(
        requests.get("https://gvsulakers.com/sports/womens-soccer/stats/2024").text,
        "html.parser",
    )
    html_soup_schedule = BeautifulSoup(
        requests.get(
            "https://gvsulakers.com/sports/womens-soccer/schedule/2024?grid=true"
        ).text,
        "html.parser",
    )

    most_recent_game_date = find_most_recent_past_date(
        get_womens_soccer_schedule(html_soup_schedule)
    )

    gd = get_game_data_by_date(html_soup_stats, most_recent_game_date)

    # validation
    for stat in [
        "Outcome",
        "Opponent",
        "Score",
        "Goal Scorers",
        "Attendance",
        "Overall Record",
        "Conference Record",
    ]:
        assert gd.get(stat, None) is not None, f"{stat} is not in game data!!!"

    outcome = gd.get("Outcome")
    opponent = gd.get("Opponent")
    score = gd.get("Score")
    overall_record = gd.get("Overall Record")
    conference_record = gd.get("Conference Record")
    attendance = gd.get("Attendance")
    goal_scorers = gd.get("Goal Scorers")

    # more validation
    assert isinstance(goal_scorers, list), f"invalid goal scorer data: {goal_scorers}"

    tweet_text = (
        f"GVSU Women's Soccer({outcome}) Vs. {opponent} {most_recent_game_date}\n\n"
        f"| Score: {score}\n"
        f"| Goal Scorers: \n        {'\n        '.join(goal_scorers)}\n"
        f"| Overall Record: {overall_record}\n"
        f"| Conference Record: {conference_record}\n\n"
        f"| Fans in Attendance: {attendance}"
    )

    client.create_tweet(text=tweet_text)
