# LouiesBurner

A Twitter/X bot system for posting sports statistics and updates for Grand Valley State University athletics. The bot supports multiple sports, scraping game statistics from the GVSU Lakers website and posting detailed game summaries and season highs to Twitter/X.

## Project Structure

```
LouiesBurner/
├── __init__.py
├── sports/              # Sport-specific implementations
│   ├── __init__.py
│   ├── baseball.py     # Baseball-specific logic
│   ├── softball.py     # Softball-specific logic
│   └── sport.py        # Abstract base class for sports
├── samplePosts.txt     # Example post formats
├── schedule.py         # Game schedule handling
├── scraping.py        # Web scraping functionality
├── utils.py           # Common utilities and constants
└── x.py               # Twitter/X API integration

schedules/              # CSV schedule files
├── bsbl_25_schedule.csv
└── softball_25_schedule.csv

scripts/                # Utility scripts
└── generate_game_schedules.py

tests/                  # Test suite
├── __init__.py
└── test_schedule.py
```

## Core Components

### Sport Base Class (`sports/sport.py`)
Abstract base class defining the interface for sport-specific implementations:
- `__init__(year: int, sport: str)`: Initialize sport with year and name
- `get_season_highs_for_date()`: Retrieve season highs for a specific date
- `create_tweet_text()`: Generate formatted tweet content
- Abstract methods for sport-specific logic

### Sport Implementations
Each sport (Baseball, Softball) extends the Sport base class with specific implementations for:
- Date extraction from opponent strings
- Tweet text generation
- Season high statistics processing
- Sport-specific verbs and statistics

### Schedule Generation (`scripts/generate_game_schedules.py`)
Generates GitHub Actions workflow files based on game schedules:
- Parses CSV schedule files
- Generates cron expressions for automated checks
- Creates sport-specific workflow YAML files

### Main Script (`main.py`)
Core execution script supporting multiple sports:
- Command-line interface for sport selection
- Season highs processing and tweet generation
- Retry mechanism for failed tweet attempts
- Grouping of achievements by player

## GitHub Actions Workflows

The project uses dynamically generated workflows for each sport, created by `generate_game_schedules.py`. Each workflow:

- Runs automatically based on game schedule
- Can be manually triggered
- Checks for season highs from the previous day's games
- Posts achievements to Twitter/X

### Required Secrets
Configure these secrets in your GitHub repository:
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
4. Generate workflow files:
   ```bash
   python scripts/generate_game_schedules.py
   ```

## Usage

### Local Execution
Run the main script with specific sport and date:
```bash
python main.py -sport baseball -date 2024-03-15
```

Available arguments:
- `-sport`: Sport to process (choices: baseball, softball)
- `-date`: Date to check in ISO format (YYYY-MM-DD)

### GitHub Actions
1. Automatic execution based on game schedules
2. Manual trigger:
   - Navigate to Actions tab
   - Select sport-specific workflow
   - Click "Run workflow"

## Output Format

The bot generates sport-specific tweets containing:
- Player name
- Achievement date
- Season high statistics
- Sport-specific formatting

Example baseball tweet:
```
💪 BEAST MODE: K. Nott 💪
Dominates with 3.0 walks against Indianapolis! #AnchorUp ⚓️
```

## Dependencies
- beautifulsoup4: Web scraping
- requests: HTTP requests
- tweepy: Twitter/X API integration
- pandas: Data processing
- pyyaml: Workflow file generation

## Testing

Run the test suite:
```bash
python -m pytest tests/
```

Tests cover:
- Schedule parsing
- Date handling
- Sport-specific implementations
- Tweet text generation
