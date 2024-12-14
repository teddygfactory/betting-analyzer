from data_fetchers.odds_api_fetcher import OddsApiFetcher
import pandas as pd
from datetime import datetime, timedelta
import pytz
import numpy as np

class BettingAnalyzer:
    def __init__(self):
        self.fetcher = OddsApiFetcher()
        self.est_tz = pytz.timezone('US/Eastern')
        
    def get_todays_best_bets(self):
        """Get the best betting opportunities for today's games"""
        best_bets = []
        
        # Get NBA games and bets
        nba_games = self.fetcher.get_upcoming_games('basketball_nba')
        if not nba_games.empty:
            best_bets.extend(self._analyze_games(nba_games, 'NBA'))
            
            # Get NBA player props
            nba_props = self.fetcher.get_player_props('basketball_nba')
            if not nba_props.empty:
                best_bets.extend(self._analyze_props(nba_props, 'NBA'))
        
        # Get NFL games and bets
        nfl_games = self.fetcher.get_upcoming_games('americanfootball_nfl')
        if not nfl_games.empty:
            best_bets.extend(self._analyze_games(nfl_games, 'NFL'))
            
            # Get NFL player props
            nfl_props = self.fetcher.get_player_props('americanfootball_nfl')
            if not nfl_props.empty:
                best_bets.extend(self._analyze_props(nfl_props, 'NFL'))
        
        # Sort by expected value
        best_bets.sort(key=lambda x: x['expected_value'], reverse=True)
        return best_bets
    
    def _analyze_games(self, games_df, sport):
        """Analyze games to find the best betting opportunities"""
        opportunities = []
        
        for _, game in games_df.iterrows():
            # Analyze moneyline
            ml_odds = self._parse_ml(game['ML'])
            if ml_odds:
                prob = self._calculate_win_probability(game, ml_odds['team'])
                ev = self._calculate_expected_value(ml_odds['odds'], prob)
                if ev > 0.1:  # 10% expected value
                    opportunities.append({
                        'sport': sport,
                        'time': game['Time'],
                        'matchup': f"{game['Away']} @ {game['Home']}",
                        'bet_type': 'Moneyline',
                        'pick': f"{ml_odds['team']} {ml_odds['odds']}",
                        'line': None,
                        'odds': ml_odds['odds'],
                        'expected_value': ev,
                        'analysis': f"Strong value on {ml_odds['team']} ML ({ml_odds['odds']}) - {prob:.1%} win probability"
                    })
            
            # Analyze spread
            spread_odds = self._parse_spread(game['Spread'])
            if spread_odds:
                prob = self._calculate_spread_probability(game, spread_odds)
                ev = self._calculate_expected_value(spread_odds['odds'], prob)
                if ev > 0.12:  # 12% expected value for spreads
                    opportunities.append({
                        'sport': sport,
                        'time': game['Time'],
                        'matchup': f"{game['Away']} @ {game['Home']}",
                        'bet_type': 'Spread',
                        'pick': f"{spread_odds['team']} {spread_odds['points']}",
                        'line': spread_odds['points'],
                        'odds': spread_odds['odds'],
                        'expected_value': ev,
                        'analysis': f"Strong spread value on {spread_odds['team']} {spread_odds['points']} ({spread_odds['odds']}) - {prob:.1%} cover probability"
                    })
            
            # Analyze totals
            total_odds = self._parse_total(game['Total'])
            if total_odds:
                prob = self._calculate_total_probability(game, total_odds)
                ev = self._calculate_expected_value(total_odds['odds'], prob)
                if ev > 0.12:  # 12% expected value for totals
                    opportunities.append({
                        'sport': sport,
                        'time': game['Time'],
                        'matchup': f"{game['Away']} @ {game['Home']}",
                        'bet_type': 'Total',
                        'pick': f"{'Over' if total_odds['pick'] == 'Over' else 'Under'} {total_odds['total']}",
                        'line': total_odds['total'],
                        'odds': total_odds['odds'],
                        'expected_value': ev,
                        'analysis': f"Strong value on {total_odds['pick']} {total_odds['total']} ({total_odds['odds']}) - {prob:.1%} probability"
                    })
        
        return opportunities
    
    def _analyze_props(self, props_df, sport):
        """Analyze player props to find the best betting opportunities"""
        opportunities = []
        
        for _, prop in props_df.iterrows():
            over_odds = int(prop['Over']) if pd.notna(prop['Over']) else None
            under_odds = int(prop['Under']) if pd.notna(prop['Under']) else None
            
            if over_odds:
                prob = self._calculate_prop_probability(prop, 'Over')
                ev = self._calculate_expected_value(over_odds, prob)
                if ev > 0.15:  # 15% expected value for props
                    opportunities.append({
                        'sport': sport,
                        'time': prop['Time'],
                        'matchup': prop['Game'],
                        'bet_type': f"Player Prop - {prop['Type']}",
                        'pick': f"{prop['Player']} Over {prop['Line']}",
                        'line': prop['Line'],
                        'odds': over_odds,
                        'expected_value': ev,
                        'analysis': f"Strong value on {prop['Player']} Over {prop['Line']} {prop['Type']} ({over_odds}) - {prob:.1%} probability"
                    })
            
            if under_odds:
                prob = self._calculate_prop_probability(prop, 'Under')
                ev = self._calculate_expected_value(under_odds, prob)
                if ev > 0.15:  # 15% expected value for props
                    opportunities.append({
                        'sport': sport,
                        'time': prop['Time'],
                        'matchup': prop['Game'],
                        'bet_type': f"Player Prop - {prop['Type']}",
                        'pick': f"{prop['Player']} Under {prop['Line']}",
                        'line': prop['Line'],
                        'odds': under_odds,
                        'expected_value': ev,
                        'analysis': f"Strong value on {prop['Player']} Under {prop['Line']} {prop['Type']} ({under_odds}) - {prob:.1%} probability"
                    })
        
        return opportunities
    
    def _parse_ml(self, ml_str):
        """Parse moneyline odds string"""
        try:
            if not ml_str:
                return None
            odds = ml_str.split('/')
            odds1 = int(odds[0])
            odds2 = int(odds[1])
            
            # Find the better value
            prob1 = self._odds_to_probability(odds1)
            prob2 = self._odds_to_probability(odds2)
            
            return {
                'team': 'Away' if prob1 < prob2 else 'Home',
                'odds': odds1 if prob1 < prob2 else odds2,
                'implied_prob': min(prob1, prob2)
            }
        except:
            return None
    
    def _parse_spread(self, spread_str):
        """Parse spread odds string"""
        try:
            if not spread_str:
                return None
            parts = spread_str.split(' ')
            points = float(parts[0])
            odds = int(parts[1].strip('()'))
            
            return {
                'team': 'Favorite' if points < 0 else 'Underdog',
                'points': points,
                'odds': odds,
                'implied_prob': self._odds_to_probability(odds)
            }
        except:
            return None
    
    def _parse_total(self, total_str):
        """Parse total odds string"""
        try:
            if not total_str:
                return None
            parts = total_str.split(' ')
            total = float(parts[1])
            odds = int(parts[2].strip('()'))
            over_prob = self._odds_to_probability(odds)
            
            return {
                'total': total,
                'odds': odds,
                'pick': 'Over' if over_prob > 0.5 else 'Under',
                'implied_prob': over_prob
            }
        except:
            return None
    
    def _odds_to_probability(self, american_odds):
        """Convert American odds to implied probability"""
        if american_odds > 0:
            return 100 / (american_odds + 100)
        else:
            return abs(american_odds) / (abs(american_odds) + 100)
    
    def _calculate_expected_value(self, odds, probability):
        """Calculate expected value of a bet"""
        if odds > 0:
            return (odds/100 * probability) - (1 - probability)
        else:
            return (probability - ((abs(odds)/100) * (1 - probability)))
    
    def _calculate_win_probability(self, game, team):
        """Calculate win probability based on various factors"""
        # This should be enhanced with historical data, team stats, etc.
        # For now using a simple model based on implied probability
        ml_odds = self._parse_ml(game['ML'])
        return 1 - ml_odds['implied_prob']  # Basic contrarian approach
    
    def _calculate_spread_probability(self, game, spread_odds):
        """Calculate probability of covering the spread"""
        # This should be enhanced with historical ATS data, team stats, etc.
        return 0.55 if abs(spread_odds['points']) < 7 else 0.45
    
    def _calculate_total_probability(self, game, total_odds):
        """Calculate probability of over/under hitting"""
        # This should be enhanced with historical O/U data, team stats, etc.
        return 0.52 if total_odds['pick'] == 'Over' else 0.48
    
    def _calculate_prop_probability(self, prop, side):
        """Calculate probability of a player prop hitting"""
        # Get the implied probability from the odds
        if side == 'Over':
            implied_prob = self._odds_to_probability(int(prop['Over'])) if pd.notna(prop['Over']) else 0.5
        else:
            implied_prob = self._odds_to_probability(int(prop['Under'])) if pd.notna(prop['Under']) else 0.5
        
        # Adjust probability based on prop type and historical trends
        base_prob = implied_prob
        
        if prop['Type'] == 'Points':
            # Points tend to go over slightly more often
            base_prob = base_prob * 1.05 if side == 'Over' else base_prob * 0.95
        elif prop['Type'] == 'Rebounds':
            # Rebounds are more volatile
            base_prob = base_prob * 1.02 if side == 'Over' else base_prob * 0.98
        elif prop['Type'] == 'Assists':
            # Assists are more predictable
            base_prob = base_prob * 1.01 if side == 'Over' else base_prob * 0.99
        elif prop['Type'] == 'Pass Tds':
            # Passing TDs are more volatile
            base_prob = base_prob * 1.03 if side == 'Over' else base_prob * 0.97
        elif prop['Type'] == 'Receptions':
            # Receptions are more predictable
            base_prob = base_prob * 1.01 if side == 'Over' else base_prob * 0.99
        
        # Cap probability at reasonable limits
        return min(max(base_prob, 0.35), 0.75)

if __name__ == "__main__":
    analyzer = BettingAnalyzer()
    best_bets = analyzer.get_todays_best_bets()
    
    print("\nBest Betting Opportunities Today:")
    print("=================================")
    
    for bet in best_bets[:10]:  # Show top 10 bets
        print(f"\n{bet['sport']} - {bet['time']}")
        print(f"Matchup: {bet['matchup']}")
        print(f"Bet Type: {bet['bet_type']}")
        print(f"Pick: {bet['pick']}")
        print(f"Analysis: {bet['analysis']}")
        print("Expected Value: {:.1%}".format(bet['expected_value']))
