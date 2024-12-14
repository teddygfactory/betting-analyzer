from typing import Dict, List, Optional
import numpy as np
from datetime import datetime, timedelta
from sports_config import NBA_CONFIG, NFL_CONFIG, STAT_WEIGHTS

class BettingStrategy:
    def __init__(self):
        self.min_confidence = 0.65  # Minimum confidence threshold for bet recommendations
        self.max_risk_ratio = 0.1   # Maximum portion of bankroll to risk on single bet

    def analyze_spread_bet(self, team_stats: Dict, opponent_stats: Dict, spread: float) -> Dict:
        """Analyze point spread betting opportunity"""
        confidence = self._calculate_spread_confidence(team_stats, opponent_stats, spread)
        return {
            'recommendation': 'bet' if confidence > self.min_confidence else 'pass',
            'confidence': confidence,
            'factors': self._get_spread_factors(team_stats, opponent_stats)
        }

    def analyze_totals_bet(self, team_stats: Dict, opponent_stats: Dict, total_line: float) -> Dict:
        """Analyze over/under betting opportunity"""
        confidence = self._calculate_totals_confidence(team_stats, opponent_stats, total_line)
        return {
            'recommendation': 'bet' if confidence > self.min_confidence else 'pass',
            'confidence': confidence,
            'factors': self._get_totals_factors(team_stats, opponent_stats)
        }

    def analyze_player_props(self, player_stats: Dict, opponent_stats: Dict, prop_line: float, prop_type: str) -> Dict:
        """Analyze player proposition betting opportunity"""
        confidence = self._calculate_prop_confidence(player_stats, opponent_stats, prop_line, prop_type)
        return {
            'recommendation': 'bet' if confidence > self.min_confidence else 'pass',
            'confidence': confidence,
            'factors': self._get_prop_factors(player_stats, opponent_stats, prop_type)
        }

class NBABettingStrategy(BettingStrategy):
    def __init__(self):
        super().__init__()
        self.pace_factor_weight = 0.2
        self.rest_days_weight = 0.15
        self.home_court_weight = 0.1

    def _calculate_spread_confidence(self, team_stats: Dict, opponent_stats: Dict, spread: float) -> float:
        """Calculate confidence level for NBA spread bet"""
        factors = [
            self._analyze_pace_matchup(team_stats, opponent_stats),
            self._analyze_rest_advantage(team_stats, opponent_stats),
            self._analyze_home_court_impact(team_stats),
            self._analyze_injury_impact(team_stats, opponent_stats)
        ]
        return np.mean(factors)

    def _analyze_pace_matchup(self, team_stats: Dict, opponent_stats: Dict) -> float:
        """Analyze how team pace factors match up"""
        # Implementation for pace analysis
        return 0.0

    def _analyze_rest_advantage(self, team_stats: Dict, opponent_stats: Dict) -> float:
        """Analyze impact of rest days between games"""
        # Implementation for rest days analysis
        return 0.0

    def _get_prop_factors(self, player_stats: Dict, opponent_stats: Dict, prop_type: str) -> Dict:
        """Get relevant factors for NBA player props"""
        return {
            'usage_rate': self._calculate_usage_rate(player_stats),
            'matchup_advantage': self._calculate_matchup_advantage(player_stats, opponent_stats),
            'recent_form': self._analyze_recent_form(player_stats),
            'pace_impact': self._analyze_pace_impact(player_stats, opponent_stats)
        }

class NFLBettingStrategy(BettingStrategy):
    def __init__(self):
        super().__init__()
        self.weather_weight = 0.15
        self.turnover_weight = 0.2
        self.injury_weight = 0.25

    def _calculate_spread_confidence(self, team_stats: Dict, opponent_stats: Dict, spread: float) -> float:
        """Calculate confidence level for NFL spread bet"""
        factors = [
            self._analyze_weather_impact(team_stats),
            self._analyze_turnover_differential(team_stats, opponent_stats),
            self._analyze_injury_impact(team_stats, opponent_stats),
            self._analyze_defensive_matchup(team_stats, opponent_stats)
        ]
        return np.mean(factors)

    def _analyze_weather_impact(self, team_stats: Dict) -> float:
        """Analyze impact of weather conditions"""
        # Implementation for weather analysis
        return 0.0

    def _analyze_turnover_differential(self, team_stats: Dict, opponent_stats: Dict) -> float:
        """Analyze turnover differential impact"""
        # Implementation for turnover analysis
        return 0.0

    def _get_prop_factors(self, player_stats: Dict, opponent_stats: Dict, prop_type: str) -> Dict:
        """Get relevant factors for NFL player props"""
        return {
            'defensive_ranking': self._calculate_defensive_ranking(opponent_stats, prop_type),
            'usage_trend': self._analyze_usage_trend(player_stats),
            'weather_impact': self._analyze_weather_impact_on_props(player_stats),
            'injury_status': self._check_injury_status(player_stats)
        }

class BettingStrategyFactory:
    @staticmethod
    def create_strategy(sport: str) -> BettingStrategy:
        if sport.upper() == 'NBA':
            return NBABettingStrategy()
        elif sport.upper() == 'NFL':
            return NFLBettingStrategy()
        else:
            raise ValueError(f"Unsupported sport: {sport}")
