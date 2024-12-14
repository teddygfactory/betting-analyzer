import pandas as pd
import requests
import os

class OddsApiFetcher:
    def __init__(self):
        self.api_key = os.environ.get('ODDS_API_KEY')
        
    def get_upcoming_games(self, sport):
        """Get upcoming games for a sport"""
        return pd.DataFrame()  # Return empty DataFrame for now
        
    def get_player_props(self, sport):
        """Get player props for a sport"""
        return pd.DataFrame()  # Return empty DataFrame for now
