import sys
import os
import pytest
import datetime
import pandas as pd

sys.path.append(os.path.abspath(".."))

from LouiesBurner.sports.baseball import Baseball
from LouiesBurner.sports.softball import Softball


def test_baseball_initialization():
    """Test Baseball class initialization"""
    baseball = Baseball(2024)
    assert baseball.year == 2024
    assert baseball.url == "https://gvsulakers.com/sports/baseball/stats/2024"


def test_softball_initialization():
    """Test Softball class initialization"""
    softball = Softball(2024)
    assert softball.year == 2024
    assert softball.url == "https://gvsulakers.com/sports/softball/stats/2024"


def test_baseball_verb_selection():
    """Test baseball-specific verb selection"""
    baseball = Baseball(2024)
    assert baseball._get_baseball_verb("HITS") == "racked up"
    assert baseball._get_baseball_verb("HOME RUNS") == "crushed"
    assert baseball._get_baseball_verb("STOLEN BASES") == "swiped"
    assert baseball._get_baseball_verb("INNINGS PITCHED") == "dominated for"
    assert baseball._get_baseball_verb("UNKNOWN STAT") == "recorded"


def test_softball_verb_selection():
    """Test softball-specific verb selection"""
    softball = Softball(2024)
    assert softball._get_softball_verb("AT BATS") == "finished with"
    assert softball._get_softball_verb("HITS") == "racked up"
    assert softball._get_softball_verb("HOME RUNS") == "crushed"
    assert softball._get_softball_verb("WALKS") == "drew"
    assert softball._get_softball_verb("UNKNOWN STAT") == "recorded"


def test_baseball_negative_stats():
    """Test baseball negative stats filtering"""
    baseball = Baseball(2024)
    assert baseball._should_tweet_stat("HITS") == True
    assert baseball._should_tweet_stat("HOME RUNS") == True
    assert baseball._should_tweet_stat("STRIKEOUTS") == False
    assert baseball._should_tweet_stat("WILD PITCHES") == False


def test_softball_negative_stats():
    """Test softball negative stats filtering"""
    softball = Softball(2024)
    assert softball._should_tweet_stat("HITS") == True
    assert softball._should_tweet_stat("HOME RUNS") == True
    assert softball._should_tweet_stat("STRIKEOUTS") == False
    assert softball._should_tweet_stat("CAUGHT STEALING") == False


def test_baseball_date_extraction():
    """Test baseball date extraction from opponent string"""
    baseball = Baseball(2024)
    test_date = baseball._extract_date("Team Name (3/15/2024)")
    assert isinstance(test_date, datetime.date)
    assert test_date == datetime.date(2024, 3, 15)
    assert baseball._extract_date("Invalid Format") is None


def test_softball_date_extraction():
    """Test softball date extraction from opponent string"""
    softball = Softball(2024)
    test_date = softball._extract_date("Team Name (3/15/2024)")
    assert isinstance(test_date, datetime.date)
    assert test_date == datetime.date(2024, 3, 15)
    assert softball._extract_date("Invalid Format") is None


def test_baseball_tweet_creation():
    """Test baseball tweet creation"""
    baseball = Baseball(2024)
    high = [
        {
            "Player": "John Doe",
            "Value": 3,
            "Statistic": "HOME RUNS",
            "Opponent": "Team A (3/15/2024)",
        }
    ]
    tweet = baseball.create_tweet_text(high)
    assert "John Doe" in tweet
    assert "3" in tweet
    assert "home runs" in tweet
    assert "Team A" in tweet
    assert "#AnchorUp" in tweet


def test_softball_tweet_creation():
    """Test softball tweet creation"""
    softball = Softball(2024)
    high = [
        {
            "Player": "Jane Doe",
            "Value": 4,
            "Statistic": "HITS",
            "Opponent": "Team B (3/15/2024)",
        }
    ]
    tweet = softball.create_tweet_text(high)
    assert "Jane Doe" in tweet
    assert "4" in tweet
    assert "hits" in tweet
    assert "Team B" in tweet
    assert "#AnchorUp" in tweet


def test_baseball_integration():
    """Integration test for baseball season highs workflow"""
    baseball = Baseball(2024)

    # Mock the season_high_df property with test data
    test_data = {
        "Statistic": ["HOME RUNS", "HITS", "STRIKEOUTS"],
        "High": [3, 4, 10],
        "Player": ["John Doe", "Jane Smith", "Bob Johnson"],
        "Opponent": ["Team A (3/15/2024)", "Team B (3/15/2024)", "Team C (3/15/2024)"],
    }
    baseball._szn_high_df = pd.DataFrame(test_data)

    # Test getting season highs for the next day (3/16/2024)
    test_date = datetime.date(2024, 3, 16)
    highs = baseball.get_season_highs_for_date(test_date)

    # Verify we got the expected results
    assert (
        len(highs) == 2
    )  # Should only get HOME RUNS and HITS (STRIKEOUTS is negative)

    # Test the first high (HOME RUNS)
    assert highs[0]["Statistic"] == "HOME RUNS"
    assert highs[0]["Value"] == 3
    assert highs[0]["Player"] == "John Doe"

    # Create and verify tweet
    tweet = baseball.create_tweet_text([highs[0]])
    assert "John Doe" in tweet
    assert "3" in tweet
    assert "home runs" in tweet
    assert "#AnchorUp" in tweet


def test_softball_integration():
    """Integration test for softball season highs workflow"""
    softball = Softball(2024)

    # Mock the season_high_df property with test data
    test_data = {
        "Statistic": ["HITS", "WALKS", "STRIKEOUTS"],
        "High": [4, 3, 2],
        "Player": ["Jane Smith", "Sarah Jones", "Amy Brown"],
        "Opponent": ["Team X (3/15/2024)", "Team Y (3/15/2024)", "Team Z (3/15/2024)"],
    }
    softball._szn_high_df = pd.DataFrame(test_data)

    # Test getting season highs for the next day (3/16/2024)
    test_date = datetime.date(2024, 3, 16)
    highs = softball.get_season_highs_for_date(test_date)

    # Verify we got the expected results
    assert len(highs) == 2  # Should only get HITS and WALKS (STRIKEOUTS is negative)

    # Test the first high (HITS)
    assert highs[0]["Statistic"] == "HITS"
    assert highs[0]["Value"] == 4
    assert highs[0]["Player"] == "Jane Smith"

    # Create and verify tweet
    tweet = softball.create_tweet_text([highs[0]])
    assert "Jane Smith" in tweet
    assert "4" in tweet
    assert "hits" in tweet
    assert "#AnchorUp" in tweet
