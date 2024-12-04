import csv
from datetime import datetime, timedelta
import yaml
from pathlib import Path


def parse_schedule(csv_file):
    game_dates = set()
    with open(csv_file, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                game_date = datetime.strptime(row["Start Date"], "%m/%d/%Y")
                game_dates.add(game_date)
            except ValueError:
                continue
    return sorted(list(game_dates))


def generate_cron_schedule(game_dates):
    # get the day after each game at 12:00 UTC
    check_dates = [game_date + timedelta(days=1) for game_date in game_dates]
    cron_expressions = []
    for date in check_dates:
        # Format: minute hour day month day-of-week
        cron_expressions.append(f"0 12 {date.day} {date.month} *")
    return cron_expressions


def create_workflow_file(name, sport, cron_expressions):
    workflow = {
        "name": f"{name} Season Highs Check",
        "on": {"schedule": [{"cron": expr} for expr in cron_expressions]},
        "jobs": {
            "check-season-highs": {
                "runs-on": "ubuntu-latest",
                "steps": [
                    {"uses": "actions/checkout@v4"},
                    {
                        "name": "Set up Python",
                        "uses": "actions/setup-python@v4",
                        "with": {"python-version": "3.12"},
                    },
                    {
                        "name": "Install dependencies",
                        "run": "python -m pip install --upgrade pip\npip install -r requirements.txt",
                    },
                    {
                        "name": "Check for new season highs",
                        "run": f"python main.py -sport {sport}",
                        "env": {
                            "CLIENT_ID": "${{ secrets.CLIENT_ID }}",
                            "CLIENT_SECRET": "${{ secrets.CLIENT_SECRET }}",
                            "BEARER_TOKEN": "${{ secrets.BEARER_TOKEN }}",
                            "ACCESS_TOKEN": "${{ secrets.ACCESS_TOKEN }}",
                            "ACCESS_TOKEN_SECRET": "${{ secrets.ACCESS_TOKEN_SECRET }}",
                            "CONSUMER_KEY": "${{ secrets.CONSUMER_KEY }}",
                            "CONSUMER_SECRET": "${{ secrets.CONSUMER_SECRET }}",
                        },
                    },
                ],
            }
        },
    }
    return workflow


def main():
    # Create workflows directory if it doesn't exist
    Path(".github/workflows").mkdir(parents=True, exist_ok=True)

    # Baseball schedule
    baseball_dates = parse_schedule("schedules/bsbl_25_schedule.csv")
    baseball_cron = generate_cron_schedule(baseball_dates)
    baseball_workflow = create_workflow_file("Baseball", "baseball", baseball_cron)

    with open(".github/workflows/baseball.yml", "w") as f:
        yaml.dump(baseball_workflow, f, sort_keys=False)

    # Softball schedule
    softball_dates = parse_schedule("schedules/softball_25_schedule.csv")
    softball_cron = generate_cron_schedule(softball_dates)
    softball_workflow = create_workflow_file("Softball", "softball", softball_cron)

    with open(".github/workflows/softball.yml", "w") as f:
        yaml.dump(softball_workflow, f, sort_keys=False)


if __name__ == "__main__":
    main()
