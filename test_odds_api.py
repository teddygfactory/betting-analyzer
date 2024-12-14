from data_fetchers.odds_api_fetcher import OddsApiFetcher
import pandas as pd

def test_odds_api():
    fetcher = OddsApiFetcher()
    
    # Test getting available sports
    print("\nAvailable sports:")
    sports = fetcher.get_available_sports()
    print(sports)
    
    # Test getting upcoming NBA games
    print("\nUpcoming NBA games:")
    games = fetcher.get_upcoming_games('basketball_nba')
    if not games.empty:
        print("\nNBA Games:")
        print(games[['Time', 'Home', 'Away', 'Spread', 'Total', 'ML']])
    else:
        print("No upcoming NBA games found")
    
    # Test getting NFL games
    print("\nUpcoming NFL games:")
    games = fetcher.get_upcoming_games('americanfootball_nfl')
    if not games.empty:
        print("\nNFL Games:")
        print(games[['Time', 'Home', 'Away', 'Spread', 'Total', 'ML']])
    else:
        print("No upcoming NFL games found")

if __name__ == "__main__":
    test_odds_api()
