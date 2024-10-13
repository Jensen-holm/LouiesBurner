import requests
from bs4 import BeautifulSoup

URL = "https://gvsulakers.com/sports/womens-soccer/stats/2024"
page = requests.get(URL)
html_soup = BeautifulSoup(page.text, "html.parser")
game_results_section = html_soup.find('section', id='game-results')  

date_to_check = "10/11/2024"  # Change to the find game data from desired date

def get_goals_scored_by_date(date: str="MM/DD/YYYY"):

    if game_results_section:                                        
        rows = game_results_section.find_all('tr')                  

        for row in rows: 
            date_cell = row.find('td')        # date is in the first <td> of each <tr>
            if date_cell and date_cell.text.strip() == date:
                goals_cell = row.find('td', {'data-label': 'Goals Scored [Assist]'})
                if goals_cell:
                    scorers = []
                    for scorer in goals_cell.stripped_strings:  # individual goal scorers
                        scorers.append(scorer)
                    return scorers  # list of goal scorers
    return "No data found for the specified date."

def get_attendance_by_date(date: str="MM/DD/YYYY"):

    if game_results_section:
        rows = game_results_section.find_all('tr')
        for row in rows:
            date_cell = row.find('td')  #date is in the first <td> of each <tr>
            if date_cell and date_cell.text.strip() == date:
                attendance_cell = row.find('td', {'data-label': 'Attend'})
                if attendance_cell:
                    return attendance_cell.text.strip()  # Return the attendance value
    return "No data found for the specified date."

def get_score_by_date(date: str="MM/DD/YYYY"):

    if game_results_section:
        rows = game_results_section.find_all('tr')
        for row in rows:
            date_cell = row.find('td')  #date is in the first <td> of each <tr>
            if date_cell and date_cell.text.strip() == date:
                score_cell = row.find('td', {'data-label': 'Score'})
                if score_cell:
                    return score_cell.text.strip()  # Return the attendance value
    return "No data found for the specified date."

def get_opponent_name(date):

    rows = game_results_section.find_all('tr')
    for row in rows:
        date_cell = row.find('td')  #date is in the first <td> of each <tr>
        if date_cell and date_cell.text.strip() == date:
            opponent_cell = row.find_all('td')[1]  #opponent is in the second <td>
            if opponent_cell:
                opponent_name = opponent_cell.find('a').text   #find text of the <a> tag
                return opponent_name.strip()

    print("No matching date found in game results.")
    return None

def get_outcome(date):

    rows = game_results_section.find_all('tr')
    for row in rows:
        date_cell = row.find('td')  #date is in the first <td> of each <tr>
        if date_cell and date_cell.text.strip() == date:
            outcome_cell = row.find_all('td')[2]  #outcome is in the third <td>
            if outcome_cell:
                outcome = outcome_cell.text.strip() #extract text
                return outcome  # return W or L


goals_scored = get_goals_scored_by_date(date_to_check)
attendance = get_attendance_by_date(date_to_check)
opponent = get_opponent_name(date_to_check)
outcome = get_outcome(date_to_check)
score = get_score_by_date(date_to_check)

print(f"\nGVSU Women's Soccer({outcome}) Vs. {opponent} on {date_to_check}:\n\n | Score: {score}  |\n | Goal Scorers: {goals_scored} |\n | Attendance: {attendance} |\n")


