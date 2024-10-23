from x_api import client
import datetime
from main import get_game_data_by_date, html_soup

results = get_game_data_by_date(html_soup, "09/07/2024")
tweet_text = f"GVSU Women's Soccer({results['Outcome']}) Vs. {results['Opponent']} on 09/07/2024:\n\n | Score: {results['Score']}  |\n | Goal Scorers: {results['Goal Scorers']} |\n | Attendance: {results['Attendance']} |\n | Overall Record: {results['Overall Record']} |\n | Conference Record: {results['Conference Record']} |\n"


client.create_tweet(text=tweet_text)