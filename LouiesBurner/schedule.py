import requests
from bs4 import BeautifulSoup
from datetime import datetime


def get_womens_soccer_schedule(soup: BeautifulSoup):
    """
    Returns list of dates of all GVSU women's soccer games

            Parameters:
                    soup (BeautifulSoup): parsed html

            Returns:
                    dates_list (list): list of dates for all GVSU women's soccer games
    """
    dates_list = []
    rows = soup.find_all("tr", class_="sidearm-schedule-game")

    for row in rows:
        date_td = row.find("td")  # first <td> in the row
        if date_td:
            game_date = date_td.text.strip()
            parsed_date = datetime.strptime(
                game_date.split("(")[0].strip(), "%B %d, %Y"
            )
            formatted_date = parsed_date.strftime(
                "%m/%d/%Y"
            )  # Convert to MM/DD/YYYY format
            dates_list.append(formatted_date)
    return dates_list


def find_most_recent_past_date(dates):
    """
    Returns date of most recent GVSU women's soccer game

            Parameters:
                    dates (list): list of dates from all women's GVSU soccer game

            Returns:
                    date (str): date of most recent game
    """
    current_date = datetime.now()
    past_dates = [
        datetime.strptime(date, "%m/%d/%Y")
        for date in dates
        if datetime.strptime(date, "%m/%d/%Y") < current_date
    ]
    return max(past_dates).strftime("%m/%d/%Y")
