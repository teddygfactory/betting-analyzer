import requests
from bs4 import BeautifulSoup
import pandas as pd
from typing import Dict, List, Optional
import json
import time
from datetime import datetime

class HardRockFetcher:
    def __init__(self):
        self.base_url = "https://www.hardrocksportsbook.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Origin': 'https://www.hardrocksportsbook.com',
            'Referer': 'https://www.hardrocksportsbook.com/',
            'X-Client-Type': 'web',
            'X-Client-Version': '1.0.0'
        }
        self._get_auth_token()
        
    def _get_auth_token(self):
        """Get authentication token"""
        try:
            auth_url = f"{self.base_url}/api/auth/anonymous"
            response = requests.post(auth_url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            self.headers['Authorization'] = f"Bearer {data['token']}"
        except Exception as e:
            print(f"Error getting auth token: {e}")
            self.headers['Authorization'] = ''
    
    def get_live_games(self) -> pd.DataFrame:
        """Fetch live games from Hard Rock Sportsbook"""
        try:
            # Get live games
            sports = ['NBA', 'NFL']  # Add more leagues as needed
            games_data = []
            
            for sport in sports:
                url = f"{self.base_url}/api/sports/events/live/{sport}"
                response = requests.get(url, headers=self.headers)
                response.raise_for_status()
                
                data = response.json()
                for event in data.get('events', []):
                    game = {
                        'Sport': sport,
                        'Time': self._format_game_time(event),
                        'Home': event.get('participants', {}).get('home', {}).get('name', ''),
                        'Away': event.get('participants', {}).get('away', {}).get('name', ''),
                        'Score': self._format_score(event),
                        'Spread': self._get_market_odds(event, 'spread'),
                        'Total': self._get_market_odds(event, 'total'),
                        'ML': self._get_market_odds(event, 'moneyline')
                    }
                    games_data.append(game)
            
            return pd.DataFrame(games_data)
        except Exception as e:
            print(f"Error fetching live games: {e}")
            return pd.DataFrame()
    
    def get_player_props(self) -> pd.DataFrame:
        """Fetch player props from Hard Rock Sportsbook"""
        try:
            sports = ['NBA', 'NFL']
            props_data = []
            
            for sport in sports:
                url = f"{self.base_url}/api/sports/events/featured/{sport}/player-props"
                response = requests.get(url, headers=self.headers)
                response.raise_for_status()
                
                data = response.json()
                for market in data.get('markets', []):
                    prop = {
                        'Sport': sport,
                        'Player': market.get('participant', {}).get('name', ''),
                        'Team': market.get('participant', {}).get('team', {}).get('abbreviation', ''),
                        'Game': self._format_game_name(market),
                        'Prop Type': market.get('type', ''),
                        'Line': market.get('line', ''),
                        'Over Odds': self._format_odds(market.get('overOdds')),
                        'Under Odds': self._format_odds(market.get('underOdds'))
                    }
                    props_data.append(prop)
            
            return pd.DataFrame(props_data)
        except Exception as e:
            print(f"Error fetching player props: {e}")
            return pd.DataFrame()
    
    def _format_game_time(self, event: Dict) -> str:
        """Format game time from event data"""
        period = event.get('period', {}).get('number', '')
        time = event.get('clock', {}).get('displayValue', '')
        
        if period and time:
            period_name = 'Q' if event.get('sport') == 'NBA' else 'P'
            return f"{period_name}{period} {time}"
        return ""
    
    def _format_score(self, event: Dict) -> str:
        """Format score from event data"""
        home = event.get('participants', {}).get('home', {}).get('score', 0)
        away = event.get('participants', {}).get('away', {}).get('score', 0)
        return f"{home}-{away}"
    
    def _get_market_odds(self, event: Dict, market_type: str) -> str:
        """Get odds for a specific market type"""
        markets = event.get('markets', [])
        for market in markets:
            if market.get('type') == market_type:
                if market_type == 'moneyline':
                    home = self._format_odds(market.get('outcomes', {}).get('home', {}).get('odds'))
                    away = self._format_odds(market.get('outcomes', {}).get('away', {}).get('odds'))
                    return f"{home}/{away}"
                elif market_type == 'spread':
                    line = market.get('line', 0)
                    odds = self._format_odds(market.get('outcomes', {}).get('home', {}).get('odds'))
                    return f"{line:g} ({odds})"
                elif market_type == 'total':
                    line = market.get('line', 0)
                    odds = self._format_odds(market.get('outcomes', {}).get('over', {}).get('odds'))
                    return f"O/U {line:g} ({odds})"
        return ""
    
    def _format_odds(self, odds: Optional[float]) -> str:
        """Format odds value"""
        if odds is None:
            return ""
        return f"+{odds:g}" if odds > 0 else f"{odds:g}"
    
    def _format_game_name(self, market: Dict) -> str:
        """Format game name from market data"""
        event = market.get('event', {})
        home = event.get('participants', {}).get('home', {}).get('name', '')
        away = event.get('participants', {}).get('away', {}).get('name', '')
        return f"{away} @ {home}"
