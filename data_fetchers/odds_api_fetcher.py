import requests
import pandas as pd
from typing import Dict, List, Optional
import json
from datetime import datetime, timezone, timedelta
import os
from dotenv import load_dotenv

class OddsApiFetcher:
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the fetcher with API key from env or parameter"""
        load_dotenv()
        self.api_key = api_key or os.getenv('ODDS_API_KEY')
        if not self.api_key:
            raise ValueError("API key is required. Get one from https://the-odds-api.com/")
            
        self.base_url = "https://api.the-odds-api.com/v4"
        self.regions = ['us']  # us, uk, eu, au
        self.markets = ['h2h', 'spreads', 'totals']  # h2h (moneyline), spreads, totals
        self.odds_format = 'american'  # american, decimal, fractional
        
    def get_available_sports(self) -> List[str]:
        """Get list of available sports"""
        try:
            params = {'apiKey': self.api_key}
            response = requests.get(
                f"{self.base_url}/sports",
                params=params
            )
            response.raise_for_status()
            
            return [sport['key'] for sport in response.json()]
            
        except Exception as e:
            print(f"Error fetching sports: {e}")
            return []
            
    def get_upcoming_games(self, sport: str = 'basketball_nba') -> pd.DataFrame:
        """Fetch upcoming games with odds from multiple bookmakers"""
        try:
            print(f"Fetching upcoming games for {sport}...")
            # Get upcoming games
            params = {
                'apiKey': self.api_key,
                'regions': ','.join(self.regions),
                'markets': ','.join(self.markets),
                'oddsFormat': self.odds_format,
                'sport': sport,
                'dateFormat': 'iso'
            }
            
            response = requests.get(
                f"{self.base_url}/sports/{sport}/odds",
                params=params
            )
            response.raise_for_status()
            
            # Process the response
            games_data = []
            current_time = datetime.now(timezone(timedelta(hours=-5)))  # Current time in EST
            print(f"Current time (EST): {current_time}")
            
            data = response.json()
            print(f"Got {len(data)} games from API")
            
            for event in data:
                # Convert game time to EST
                game_time = datetime.fromisoformat(event.get('commence_time', '').replace('Z', '+00:00'))
                game_time = game_time.astimezone(timezone(timedelta(hours=-5)))  # Convert to EST
                print(f"Game time (EST): {game_time} - {event.get('home_team')} vs {event.get('away_team')}")
                
                # Skip games that have already started
                if game_time < current_time:
                    print(f"Skipping {event.get('home_team')} vs {event.get('away_team')} - already started")
                    continue
                
                bookmakers = event.get('bookmakers', [])
                if not bookmakers:
                    print(f"No bookmakers for {event.get('home_team')} vs {event.get('away_team')}")
                    continue
                    
                # Use the first bookmaker's odds (usually most reliable)
                book = bookmakers[0]
                markets = {m['key']: m for m in book.get('markets', [])}
                
                # Format time without leading zero
                time_str = game_time.strftime('%I:%M %p').lstrip('0') + ' EST'
                
                game = {
                    'Sport': sport,
                    'Time': time_str,
                    'Home': event.get('home_team', ''),
                    'Away': event.get('away_team', ''),
                    'Score': self._get_score(event),
                    'Spread': self._format_spread(markets.get('spreads')),
                    'Total': self._format_total(markets.get('totals')),
                    'ML': self._format_moneyline(markets.get('h2h')),
                    'Last Update': event.get('last_update'),
                    'Bookmaker': book.get('title', '')
                }
                games_data.append(game)
                print(f"Added game: {game['Away']} @ {game['Home']} at {game['Time']}")
            
            # Sort by game time
            df = pd.DataFrame(games_data)
            if not df.empty:
                df['_time_sort'] = pd.to_datetime(df['Time'].str.replace(' EST', ''), format='%I:%M %p')
                df = df.sort_values('_time_sort')
                df = df.drop('_time_sort', axis=1)
                print(f"Final dataframe has {len(df)} games")
            else:
                print("No upcoming games found")
            
            return df
            
        except Exception as e:
            print(f"Error fetching upcoming games: {e}")
            import traceback
            traceback.print_exc()
            return pd.DataFrame()
    
    def get_player_props(self, sport: str = 'basketball_nba') -> pd.DataFrame:
        """Fetch player props from the API"""
        try:
            print(f"Fetching player props for {sport}...")
            
            # Set appropriate markets based on sport
            if sport == 'basketball_nba':
                markets = ['player_points', 'player_rebounds', 'player_assists']
            elif sport == 'americanfootball_nfl':
                markets = ['player_pass_tds', 'player_receptions']  # Only use supported markets
            else:
                markets = []
            
            props_data = []
            current_time = datetime.now(timezone(timedelta(hours=-5)))  # EST
            
            # First get all games to get their IDs
            params = {
                'apiKey': self.api_key,
                'regions': ','.join(self.regions),
                'markets': 'h2h',  # Just get basic game info
                'oddsFormat': self.odds_format,
                'sport': sport,
                'dateFormat': 'iso'
            }
            
            response = requests.get(
                f"{self.base_url}/sports/{sport}/odds",
                params=params
            )
            response.raise_for_status()
            games = response.json()
            
            # Now fetch props for each game
            for game in games:
                game_time = datetime.fromisoformat(game.get('commence_time', '').replace('Z', '+00:00'))
                game_time = game_time.astimezone(timezone(timedelta(hours=-5)))  # Convert to EST
                
                if game_time < current_time:
                    continue
                
                game_id = game.get('id')
                if not game_id:
                    continue
                
                # Fetch props for each market type separately for this game
                for market in markets:
                    try:
                        params = {
                            'apiKey': self.api_key,
                            'regions': ','.join(self.regions),
                            'markets': market,
                            'oddsFormat': self.odds_format,
                            'dateFormat': 'iso'
                        }
                        
                        response = requests.get(
                            f"{self.base_url}/sports/{sport}/events/{game_id}/odds",
                            params=params
                        )
                        response.raise_for_status()
                        
                        data = response.json()
                        print(f"Got props for {game['home_team']} vs {game['away_team']} - {market}")
                        
                        for book in data.get('bookmakers', []):
                            for market_data in book.get('markets', []):
                                if market_data['key'].startswith('player'):
                                    for outcome in market_data.get('outcomes', []):
                                        prop_type = market_data['key'].replace('player_', '').replace('_', ' ').title()
                                        prop = {
                                            'Time': game_time.strftime('%I:%M %p').lstrip('0') + ' EST',
                                            'Game': f"{game['away_team']} @ {game['home_team']}",
                                            'Player': outcome['description'],
                                            'Type': prop_type,
                                            'Line': outcome.get('point', 'N/A'),
                                            'Over': self._format_odds(outcome.get('price')) if outcome.get('name') == 'Over' else None,
                                            'Under': self._format_odds(outcome.get('price')) if outcome.get('name') == 'Under' else None,
                                            'Bookmaker': book['title']
                                        }
                                        props_data.append(prop)
                                        
                    except Exception as e:
                        print(f"Error fetching {market} props for game {game_id}: {e}")
                        continue
            
            df = pd.DataFrame(props_data)
            if not df.empty:
                df['_time_sort'] = pd.to_datetime(df['Time'].str.replace(' EST', ''), format='%I:%M %p')
                df = df.sort_values(['_time_sort', 'Game', 'Player', 'Type'])
                df = df.drop('_time_sort', axis=1)
                print(f"Final props dataframe has {len(df)} props")
            else:
                print("No props found")
            
            return df
            
        except Exception as e:
            print(f"Error fetching player props: {e}")
            import traceback
            traceback.print_exc()
            return pd.DataFrame()
    
    def _get_score(self, event: Dict) -> str:
        """Get score if available"""
        scores = event.get('scores', {})
        if scores:
            home = scores.get(event.get('home_team'), 0)
            away = scores.get(event.get('away_team'), 0)
            return f"{home}-{away}"
        return "Not Started"
    
    def _format_spread(self, market: Optional[Dict]) -> str:
        """Format spread odds"""
        if not market:
            return ""
            
        outcomes = market.get('outcomes', [])
        if len(outcomes) != 2:
            return ""
            
        # Find the favorite (negative spread)
        fav = min(outcomes, key=lambda x: float(x.get('point', 0)))
        
        return f"{fav['point']} ({self._format_odds(fav['price'])})"
    
    def _format_total(self, market: Optional[Dict]) -> str:
        """Format total odds"""
        if not market:
            return ""
            
        outcomes = market.get('outcomes', [])
        if len(outcomes) != 2:
            return ""
            
        # Get the over
        over = next((o for o in outcomes if o['name'] == 'Over'), None)
        if not over:
            return ""
            
        return f"O/U {over['point']} ({self._format_odds(over['price'])})"
    
    def _format_moneyline(self, market: Optional[Dict]) -> str:
        """Format moneyline odds"""
        if not market:
            return ""
            
        outcomes = market.get('outcomes', [])
        if len(outcomes) != 2:
            return ""
            
        odds = [self._format_odds(o['price']) for o in outcomes]
        return f"{odds[0]}/{odds[1]}"
    
    def _format_odds(self, odds: Optional[float]) -> str:
        """Format American odds"""
        if odds is None:
            return ""
        return f"+{int(odds)}" if odds > 0 else str(int(odds))
