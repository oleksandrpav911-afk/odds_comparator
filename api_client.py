"""
API Client for api-football.com
Handles requests to the API-Football API
"""
import requests
from typing import Dict, Optional, List
import os


class APIFootballClient:
    """Client for interacting with API-Football API"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the API client
        
        Args:
            api_key: API key for api-football.com. If not provided, will try to get from environment variable
        """
        self.api_key = api_key or os.getenv('API_FOOTBALL_KEY')
        if not self.api_key:
            raise ValueError("API key is required. Set API_FOOTBALL_KEY environment variable or pass it to constructor")
        
        self.base_url = "https://v3.football.api-sports.io"
        self.headers = {
            "x-apisports-key": self.api_key,
            "Content-Type": "application/json"
        }
    
    def get_odds(self, fixture_id: int) -> Dict:
        """
        Get odds for a specific fixture
        
        Args:
            fixture_id: The fixture ID
            
        Returns:
            Dictionary containing the odds data
        """
        url = f"{self.base_url}/odds"
        params = {"fixture": fixture_id}
        
        try:
            print(f"[DEBUG] Fetching odds - URL: {url}, Params: {params}")
            print(f"[DEBUG] Headers: {self.headers}")
            response = requests.get(url, headers=self.headers, params=params)
            print(f"[DEBUG] Response status: {response.status_code}")
            print(f"[DEBUG] Response: {response.text[:200]}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Request failed: {str(e)}")
            raise Exception(f"Error fetching odds: {str(e)}")
    
    def get_fixtures(self, date: Optional[str] = None, league: Optional[int] = None, season: Optional[int] = None) -> Dict:
        """
        Get fixtures for a specific date or league
        
        Args:
            date: Date in format YYYY-MM-DD (optional)
            league: League ID (optional)
            season: Season year (e.g., 2025) (optional)
            
        Returns:
            Dictionary containing fixtures data
        """
        url = f"{self.base_url}/fixtures"
        params = {}
        
        if date:
            params["date"] = date
        if league:
            params["league"] = league
        if season:
            params["season"] = season
        
        try:
            print(f"[DEBUG] Fetching fixtures - URL: {url}, Params: {params}")
            print(f"[DEBUG] Headers: {self.headers}")
            response = requests.get(url, headers=self.headers, params=params)
            print(f"[DEBUG] Response status: {response.status_code}")
            print(f"[DEBUG] Response: {response.text[:200]}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Request failed: {str(e)}")
            raise Exception(f"Error fetching fixtures: {str(e)}")
    
    def get_bookmakers(self) -> Dict:
        """
        Get list of available bookmakers
        
        Returns:
            Dictionary containing bookmakers data
        """
        url = f"{self.base_url}/odds/bookmakers"
        
        try:
            print(f"[DEBUG] Fetching bookmakers - URL: {url}")
            print(f"[DEBUG] Headers: {self.headers}")
            response = requests.get(url, headers=self.headers)
            print(f"[DEBUG] Response status: {response.status_code}")
            print(f"[DEBUG] Response: {response.text[:200]}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Request failed: {str(e)}")
            raise Exception(f"Error fetching bookmakers: {str(e)}")
