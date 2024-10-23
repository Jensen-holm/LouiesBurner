import requests
from bs4 import BeautifulSoup

URL = "https://gvsulakers.com/sports/womens-soccer/stats/2024"
page = requests.get(URL)
html_soup = BeautifulSoup(page.text, "html.parser")

# Gets game-to-game data by date

def get_game_data_by_date(soup, date: str="MM/DD/YYYY"):
    game_data = {}          #results dict

    game_results_section = soup.find('section', id='game-results')  

    if game_results_section:
        rows = game_results_section.find_all('tr')

        for row in rows:
            date_cell = row.find('td')
            if date_cell and date_cell.text.strip() == date:

                game_data['Opponent'] = row.find_all('td')[1].find('a').text.strip()  #opponent is in the second <td> matches <a>
                game_data['Outcome'] = row.find_all('td')[2].text.strip()
                game_data['Attendance'] = row.find('td', {'data-label': 'Attend'}).text.strip()
                goals_cell = row.find('td', {'data-label': 'Goals Scored [Assist]'})

                if goals_cell:
                    scorers = []
                    for scorer in goals_cell.stripped_strings:  # individual goal scorers
                        scorers.append(scorer)
                    game_data['Goal Scorers'] = scorers  # list of goal scorers

                game_data['Score']  = row.find('td', {'data-label': 'Score'}).text.strip()
                game_data['Overall Record']  = row.find('td', {'data-label': 'Overall'}).text.strip().split(",")[0][1:]
                game_data['Conference Record'] = row.find('td', {'data-label': 'Conference'}).text.strip()
        return game_data
    return "No data found for this date."

# Gets team stats by date

def get_offensive_stats_by_date(soup, date: str):
    game_data = {}  # results dict
    game_off_results_section = soup.find('section', id='game-game-our-offensive')
    
    if game_off_results_section:
        rows = game_off_results_section.find_all('tr')
        
        for row in rows:
            date_cell = row.find('td')
            if date_cell and date_cell.text.strip() == date:
                opponent_cell = row.find_all('td')[1]
                game_data['Opponent'] = opponent_cell.get_text(strip=True)
                if game_data['Opponent'][0] == 'a' and game_data['Opponent'][1] == 't':
                    game_data['Opponent'] = game_data['Opponent'].split('at')[1] # removes the 'at' at the start of the opponent text.
                if game_data['Opponent'][0] == 'v' and game_data['Opponent'][1] == 's':
                    game_data['Opponent'] = game_data['Opponent'].split('vs')[1] # removes the 'vs' at the start of the opponent text.
                game_data['Score'] = row.find('td', {'data-label': 'Score'}).text.strip()
                game_data['Goals'] = row.find('td', {'data-label': 'G'}).text.strip()
                game_data['Assists'] = row.find('td', {'data-label': 'A'}).text.strip()
                game_data['Points'] = row.find('td', {'data-label': 'PTS'}).text.strip()
                game_data['Shots'] = row.find('td', {'data-label': 'SH'}).text.strip()
                game_data['Shot%'] = round(float(row.find('td', {'data-label': 'Shot%'}).text.strip())*100, 1)
                game_data['SOG'] = row.find('td', {'data-label': 'SOG'}).text.strip()
                game_data['SOG%'] = row.find('td', {'data-label': 'SOG%'}).text.strip()
                game_data['YC'] = row.find('td', {'data-label': 'YC-RC'}).text.strip().split("-")[0]
                game_data['RC'] = row.find('td', {'data-label': 'YC-RC'}).text.strip().split("-")[1]
                game_data['GW'] = row.find('td', {'data-label': 'GW'}).text.strip()
                game_data['PK-ATT'] = row.find('td', {'data-label': 'PK-ATT'}).text.strip()
                game_data['Minutes'] = row.find_all('td')[-1].text.strip()
                
                return game_data

    return "No data found for this date."

# Gets list of player names

def extract_player_names(soup):
    player_names = [] #results container, will contain a list of names 
    offensive_section = soup.find('section', id='individual-overall-offensive')
    rows = offensive_section.find_all('tr')
    
    for row in rows:
        name_cell = row.find('a')
        if name_cell:
            player_names.append(name_cell.text.strip())
    
    return player_names

# Gets individual player stats by name

def get_player_stats_by_name(soup, player_name):
    offensive_section = soup.find('section', id='individual-overall-offensive')
    
    for row in offensive_section.find_all('tr'):
        name_cell = row.find('a')
        if name_cell and player_name in name_cell.text:
            stats = {
                'GP': int(row.find('td', {'data-label': 'GP'}).text),
                'GS': int(row.find('td', {'data-label': 'GS'}).text),
                'MIN': int(row.find('td', {'data-label': 'MIN'}).text),
                'G': int(row.find('td', {'data-label': 'G'}).text),
                'A': int(row.find('td', {'data-label': 'A'}).text),
                'PTS': int(row.find('td', {'data-label': 'PTS'}).text),
                'SH': int(row.find('td', {'data-label': 'SH'}).text),
                'SH%': round(float(row.find('td', {'data-label': 'SH%'}).text) * 100, 1),  # convert to percentage
                'SOG': int(row.find('td', {'data-label': 'SOG'}).text),
                'SOG%': round(float(row.find('td', {'data-label': 'SOG%'}).text) * 100, 1),  # convert to percentage
                'YC': int(row.find('td', {'data-label': 'YC-RC'}).text.split('-')[0]),  # separate yellow card
                'RC': int(row.find('td', {'data-label': 'YC-RC'}).text.split('-')[1]),  # separate red card
                'GW': int(row.find('td', {'data-label': 'GW'}).text),
                'PG-PA': row.find('td', {'data-label': 'PG-PA'}).text
            }
            return {player_name: stats}
    return {}

# Example usage of get_offensive_stats_by:
"""
print(get_offensive_stats_by_date(html_soup, "10/11/2024"))
"""

# Example usage of get_player_stats_by_name:
"""
print(get_player_stats_by_name(html_soup, "Bearden, Kennedy"))
"""

# Game Data Visualisation Print Extra
"""
print(f"GVSU Women's Soccer({results['Outcome']}) Vs. {results['Opponent']} on {date_to_check}:\n\n | Score: {results['Score']}  |\n | Goal Scorers: {results['Goal Scorers']} |\n | Attendance: {results['Attendance']} |\n | Overall Record: {results['Overall Record']} |\n | Conference Record: {results['Conference Record']} |\n")
"""

# Below is code to display team game data from every date on the dates list:
dates_of_games = ["09/05/2024","09/07/2024","09/13/2024","09/15/2024","09/20/2024","09/22/2024","09/27/2024","09/29/2024","10/04/2024","10/06/2024","10/11/2024"]
"""
for d in dates_of_games:
    r = get_game_data_by_date(html_soup, d)
    print(f'-_--_--_--_--_--_--_--_--_--_--_--_--_--_--_--_--_--_--_--_--_--_--_-')
    print(f"GVSU Women's Soccer({r['Outcome']}) Vs. {r['Opponent']} on {d}:\n\n | Score: {r['Score']}  |\n | Goal Scorers: {r['Goal Scorers']} |\n | Attendance: {r['Attendance']} |\n | Overall Record: {r['Overall Record']} |\n | Conference Record: {r['Conference Record']} |\n")

    o = get_offensive_stats_by_date(html_soup, d)
    print(f"Goals: {o['Goals']}, Assists: {o['Assists']}, Points: {o['Points']}")
    print(f"Shots: {o['Shots']}, Shot%: {o['Shot%']}%, Shots On Goal: {o['SOG']}, Shots On Goal%: {o['SOG%']}")
    print(f"Yellow Cards: {o['YC']}, Red Cards: {o['RC']}, Game-Winning Goal: {o['GW']}, Penalty Kick Attempts: {o['PK-ATT']}, Minutes: {o['Minutes']}")
print(f'-_--_--_--_--_--_--_--_--_--_--_--_--_--_--_--_--_--_--_--_--_--_--_-')
"""

# Below is code to display player data from every name on the PlayerNames list:
playerNames = extract_player_names(html_soup)
"""
for p in playerNames:
    n = get_player_stats_by_name(html_soup, p)
    print(f'-_--_--_--_--_--_--_--_--_--_--_--_--_--_--_--_--_--_--_--_--_--_--_-')
    
    player_name = list(n.keys())[0]  # Get the player name
    stats = n[player_name]  # Get the stats for that player
    
    # Print player name and statistics
    print(f"Player: {player_name}")
    print(f"Games Played: {stats['GP']}, Games Started: {stats['GS']}, Minutes: {stats['MIN']}")
    print(f"Goals: {stats['G']}, Assists: {stats['A']}, Points: {stats['PTS']}")
    print(f"Shots: {stats['SH']}, Shot%: {stats['SH%']}%, Shots On Goal: {stats['SOG']}, Shots On Goal%: {stats['SOG%']}%")
    print(f"Yellow Cards: {stats['YC']}, Red Cards: {stats['RC']}, Game-Winning Goals: {stats['GW']}, Penalty Kick Attempts: {stats['PG-PA']}")
    
print(f'-_--_--_--_--_--_--_--_--_--_--_--_--_--_--_--_--_--_--_--_--_--_--_-')
"""
