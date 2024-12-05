import sys
import os
import pytest
from bs4 import BeautifulSoup

sys.path.append(os.path.abspath(".."))

from LouiesBurner.utils import ROOT_URL, VALID_SPORTS, VALID_PAGES


def test_valid_sports():
    """Test that VALID_SPORTS contains expected values"""
    assert "football" in VALID_SPORTS
    assert "baseball" in VALID_SPORTS
    assert "invalid_sport" not in VALID_SPORTS


def test_valid_pages():
    """Test that VALID_PAGES contains expected values"""
    assert "stats" in VALID_PAGES
    assert "roster" in VALID_PAGES
    assert "schedule" in VALID_PAGES
    assert "coaches" in VALID_PAGES
    assert "invalid_page" not in VALID_PAGES


def test_root_url_formatting():
    """Test that ROOT_URL formats correctly with a sport"""
    formatted_url = ROOT_URL.format(sport="baseball")
    assert formatted_url == "https://gvsulakers.com/sports/baseball"
