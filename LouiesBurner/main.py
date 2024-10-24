from datetime import datetime

import requests
from bs4 import BeautifulSoup

from schedule import get_womens_soccer_schedule, find_most_recent_past_date
from scraping import get_game_data_by_date
from x import client

if __name__ == "__main__":
    html_soup_stats = BeautifulSoup(requests.get("https://gvsulakers.com/sports/womens-soccer/stats/2024").text, "html.parser")
    html_soup_schedule = BeautifulSoup(requests.get("https://gvsulakers.com/sports/womens-soccer/schedule/2024?grid=true").text, "html.parser")

    most_recent_game_date = find_most_recent_past_date(get_womens_soccer_schedule(html_soup_schedule))

    gd = get_game_data_by_date(html_soup_stats, most_recent_game_date)

    tweet_text = f"GVSU Women's Soccer({gd['Outcome']}) Vs. {gd['Opponent']} on {most_recent_game_date}:\n\n | Score: {gd['Score']}  \n | Goal Scorers: {gd['Goal Scorers']} \n | Overall Record: {gd['Overall Record']} \n | Conference Record: {gd['Conference Record']} \n\n Fans In Attendance: {gd['Attendance']} \n"

    client.create_tweet(text=tweet_text)
    