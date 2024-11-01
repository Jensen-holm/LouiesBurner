# GVSU Women's Soccer Stats Bot

An automated Twitter/X bot that posts updates about Grand Valley State University women's soccer games. The bot scrapes game statistics from the GVSU Lakers website and posts detailed game summaries to Twitter/X.

## Project Structure

```
LouiesBurner/
├── __init__.py
├── schedule.py      # Game schedule handling
├── scraping.py     # Web scraping functionality
├── utils.py        # Common utilities and constants
└── x.py            # Twitter/X API integration
```

## Core Components

### Schedule Management (`schedule.py`)
- `get_womens_soccer_schedule()`: Extracts game dates from GVSU's website
- `find_most_recent_past_date()`: Determines the most recent game date

### Web Scraping (`scraping.py`)
- `get_game_data_by_date()`: Retrieves general game statistics
- `get_offensive_stats_by_date()`: Fetches offensive team statistics
- `get_player_names()`: Lists all players from the season
- `get_player_stats_by_name()`: Gets individual player statistics

### Twitter Integration (`x.py`)
Handles Twitter/X API authentication and posting using the Tweepy library.

### Utilities (`utils.py`)
Contains constants and common URL patterns for the GVSU athletics website.

## GitHub Actions Workflow

The project includes an automated workflow (`womens_soccer.yml`) that can be manually triggered to post game updates:

```yaml
name: womens_soccer

on:
  workflow_dispatch: # manual trigger specification

jobs:
  run-script:
    runs-on: ubuntu-latest
    steps:
    - Uses GitHub's checkout action
    - Sets up Python 3.12
    - Installs dependencies
    - Runs the main script with required Twitter/X API credentials
```

### Required Secrets
The following secrets must be configured in your GitHub repository:
- `CLIENT_ID`
- `CLIENT_SECRET`
- `BEARER_TOKEN`
- `ACCESS_TOKEN`
- `ACCESS_TOKEN_SECRET`
- `CONSUMER_KEY`
- `CONSUMER_SECRET`

## Setup Instructions

1. Clone the repository:
    ```bash
    git clone https://github.com/Jensen-holm/LouiesBurner
    ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure Twitter/X API credentials as environment variables
4. For GitHub Actions:
   - Go to your repository's Settings > Secrets and variables > Actions
   - Add all required Twitter/X API credentials as secrets

## Usage

### Local Execution
Run the main script:
```bash
python wmns_soccer.py
```

### GitHub Actions
1. Navigate to the Actions tab in your repository
2. Select the "womens_soccer" workflow
3. Click "Run workflow"

## Output Format

The bot generates tweets with the following information:
- Game outcome
- Opponent
- Date
- Score
- Goal scorers
- Overall record
- Conference record
- Attendance

Example tweet format:
```
GVSU Women's Soccer(W) Vs. [Opponent] MM/DD/YYYY

| Score: 2-1
| Goal Scorers: 
        Player 1
        Player 2
| Overall Record: 15-1-2
| Conference Record: 8-0-1

| Fans in Attendance: 1234
```

## Dependencies
- beautifulsoup4: Web scraping
- requests: HTTP requests
- tweepy: Twitter/X API integration

## Function Documentation

### schedule.py

#### `get_womens_soccer_schedule(soup: BeautifulSoup)`
Returns a list of dates for all GVSU women's soccer games.
- Parameters:
  - `soup`: BeautifulSoup object of parsed HTML
- Returns:
  - List of dates in MM/DD/YYYY format

#### `find_most_recent_past_date(dates)`
Finds the most recent past game date.
- Parameters:
  - `dates`: List of game dates
- Returns:
  - Most recent past game date in MM/DD/YYYY format

### scraping.py

#### `get_game_data_by_date(soup: BeautifulSoup, date: str)`
Retrieves game data for a specific date.
- Parameters:
  - `soup`: BeautifulSoup object of parsed HTML
  - `date`: Date in MM/DD/YYYY format
- Returns:
  - Dictionary containing:
    - Opponent
    - Outcome
    - Attendance
    - Goal Scorers (list)
    - Score
    - Overall Record
    - Conference Record

#### `get_offensive_stats_by_date(soup: BeautifulSoup, date: str)`
Retrieves offensive statistics for a specific game.
- Parameters:
  - `soup`: BeautifulSoup object of parsed HTML
  - `date`: Date in MM/DD/YYYY format
- Returns:
  - Dictionary containing offensive statistics including:
    - Goals
    - Assists
    - Points
    - Shots
    - Shot percentage
    - Shots on goal
    - Yellow/Red cards
    - Game-winning goals
    - Penalty kicks
    - Minutes played

#### `get_player_names(soup: BeautifulSoup)`
Retrieves a list of all players who played in the season.
- Parameters:
  - `soup`: BeautifulSoup object of parsed HTML
- Returns:
  - List of player names

#### `get_player_stats_by_name(soup: BeautifulSoup, player_name: str)`
Retrieves season statistics for a specific player.
- Parameters:
  - `soup`: BeautifulSoup object of parsed HTML
  - `player_name`: Player's name in "LastName, FirstName" format
- Returns:
  - Dictionary containing player's season statistics including:
    - Games played/started
    - Minutes played
    - Goals/Assists/Points
    - Shots/Shot percentage
    - Cards
    - Game-winning goals
    - Penalty kicks

### x.py
Handles Twitter/X API authentication and posting. Uses environment variables for secure credential management:
- CLIENT_ID
- CLIENT_SECRET
- BEARER_TOKEN
- ACCESS_TOKEN
- ACCESS_TOKEN_SECRET
- CONSUMER_KEY
- CONSUMER_SECRET

### utils.py
Defines constants used throughout the project:
- ROOT_URL: Base URL for GVSU sports pages
- VOLLEYBALL_ROOT_URL: URL for women's volleyball
- VALID_PAGES: Set of valid page types
- VALID_SPORTS: Set of supported sports
