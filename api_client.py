import requests
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

class SportsAPIClient:
    def __init__(self):
        self.api_key = os.getenv('API_SPORTS_KEY')
        self.base_url = "https://v3.football.api-sports.io"
        self.headers = {
            'x-rapidapi-host': "v3.football.api-sports.io",
            'x-rapidapi-key': self.api_key
        }

    def get_team_statistics(self, team_id: int, league_id: int, season: int) -> Dict:
        """Get team statistics for a specific season"""
        endpoint = f"{self.base_url}/teams/statistics"
        params = {
            'team': team_id,
            'league': league_id,
            'season': season
        }
        response = requests.get(endpoint, headers=self.headers, params=params)
        return response.json()

    def get_h2h_matches(self, team1_id: int, team2_id: int) -> List[Dict]:
        """Get head-to-head matches between two teams"""
        endpoint = f"{self.base_url}/fixtures/headtohead"
        params = {
            'h2h': f"{team1_id}-{team2_id}",
            'last': 10
        }
        response = requests.get(endpoint, headers=self.headers, params=params)
        return response.json()

    def get_team_form(self, team_id: int, last_n_matches: int = 5) -> Dict:
        """Get team's recent form"""
        endpoint = f"{self.base_url}/fixtures"
        params = {
            'team': team_id,
            'last': last_n_matches
        }
        response = requests.get(endpoint, headers=self.headers, params=params)
        return response.json()

    def get_league_standings(self, league_id: int, season: int) -> Dict:
        """Get current league standings"""
        endpoint = f"{self.base_url}/standings"
        params = {
            'league': league_id,
            'season': season
        }
        response = requests.get(endpoint, headers=self.headers, params=params)
        return response.json()

    def get_player_statistics(self, player_id: int, season: int) -> Dict:
        """Get player statistics for a specific season"""
        endpoint = f"{self.base_url}/players"
        params = {
            'id': player_id,
            'season': season
        }
        response = requests.get(endpoint, headers=self.headers, params=params)
        return response.json()

    def get_live_odds(self, fixture_id: int) -> Dict:
        """Get live betting odds for a specific fixture"""
        endpoint = f"{self.base_url}/odds/live"
        params = {
            'fixture': fixture_id
        }
        response = requests.get(endpoint, headers=self.headers, params=params)
        return response.json()

    def get_fixtures_by_date(self, date: str) -> List[Dict]:
        """Get fixtures for a specific date (YYYY-MM-DD format)"""
        endpoint = f"{self.base_url}/fixtures"
        params = {
            'date': date
        }
        response = requests.get(endpoint, headers=self.headers, params=params)
        return response.json()

class TrendAnalyzer:
    def __init__(self, api_client: SportsAPIClient):
        self.api_client = api_client

    def analyze_team_form(self, team_id: int) -> Dict:
        """Analyze team's recent form and performance trends"""
        form_data = self.api_client.get_team_form(team_id)
        # Process and analyze form data
        return {
            'raw_data': form_data,
            'form_rating': self._calculate_form_rating(form_data),
            'scoring_trend': self._analyze_scoring_trend(form_data),
            'defense_trend': self._analyze_defense_trend(form_data)
        }

    def _calculate_form_rating(self, form_data: Dict) -> float:
        # Implement form rating calculation
        # This is a placeholder implementation
        return 0.0

    def _analyze_scoring_trend(self, form_data: Dict) -> Dict:
        # Implement scoring trend analysis
        # This is a placeholder implementation
        return {}

    def _analyze_defense_trend(self, form_data: Dict) -> Dict:
        # Implement defense trend analysis
        # This is a placeholder implementation
        return {}
