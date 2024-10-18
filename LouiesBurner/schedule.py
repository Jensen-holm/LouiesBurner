
import requests
from bs4 import BeautifulSoup

URL = "https://gvsulakers.com/sports/womens-soccer/schedule"
page = requests.get(URL)
html_soup = BeautifulSoup(page.text, "html.parser")


game_details = html_soup.find_all('div', class_='sidearm-schedule-game-details x-small-3 columns')

# Check if any matching elements are found
if game_details:
    for detail in game_details:
        print(detail.text.strip())  # Print the text inside the <div>
else:
    print("No matching elements found.")

"""
"""

flex_elements = html_soup.find_all('div', class_='flex flex-justify-between')

# Check if any matching elements are found
if flex_elements:
    for element in flex_elements:
        print(element.text.strip())  # Print the text inside the <div>
else:
    print("No matching elements found.")

"""
"""


opponent_text_elements = html_soup.find_all('div', class_='sidearm-schedule-game-opponent-text')

# Check if any matching elements are found
if opponent_text_elements:
    for element in opponent_text_elements:
        print(element.text.strip())  # Print the text inside the <div>
else:
    print("No matching elements found.")

"""
"""

game_row_elements = html_soup.find_all('div', class_='sidearm-schedule-game-row sidearm-schedule-game-row-desktop row flex flex-align-center')

# Check if any matching elements are found
if game_row_elements:
    for element in game_row_elements:
        # Example: Get the opponent text within this row
        opponent_text = element.find('div', class_='sidearm-schedule-game-opponent-text').text.strip()
        date_text = element.find('span').text.strip()  # Get the date
        print(f"Opponent: {opponent_text}, Date: {date_text}")  # Print both the opponent and the date
else:
    print("No matching elements found.")