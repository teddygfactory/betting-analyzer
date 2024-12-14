from betting_analyzer import BettingAnalyzer
import pandas as pd
import numpy as np
from datetime import datetime

def test_live_game_analysis():
    # Sample game data
    game_data = {
        'home_team': 'Lakers',
        'away_team': 'Celtics',
        'quarter': 2,
        'time_remaining': '5:30',
        'home_score': 45,
        'away_score': 42,
        'odds': {
            'spread': -3.5,
            'total': 220.5,
            'home_ml': -150,
            'away_ml': +130
        },
        'stats': {
            'home': {
                'fg_pct': 0.485,
                'three_pct': 0.375,
                'rebounds': 18,
                'turnovers': 6
            },
            'away': {
                'fg_pct': 0.445,
                'three_pct': 0.333,
                'rebounds': 20,
                'turnovers': 8
            }
        }
    }

    analyzer = BettingAnalyzer()
    print("\nTesting Live Game Analysis...")
    analysis = analyzer.analyze_live_game(game_data)
    print(f"Spread Prediction: {analysis['spread_prediction']:.1f}")
    print(f"Spread Confidence: {analysis['spread_confidence']:.1%}")
    print(f"Momentum Shift: {analysis['momentum_shift']:.2f}")
    print(f"Key Factors:", analysis['key_factors'])

def test_player_props():
    # Sample player data
    player_data = {
        'name': 'LeBron James',
        'team': 'Lakers',
        'season_avg': {
            'points': 25.8,
            'rebounds': 7.2,
            'assists': 7.9
        },
        'last_5_games': {
            'points': [28, 24, 31, 22, 27],
            'rebounds': [8, 6, 9, 7, 8],
            'assists': [9, 6, 8, 7, 10]
        },
        'matchup_history': {
            'points': 26.5,
            'rebounds': 7.8,
            'assists': 8.1
        }
    }

    analyzer = BettingAnalyzer()
    print("\nTesting Player Props Analysis...")
    prop_types = ['points', 'rebounds', 'assists']
    predictions = analyzer.analyze_player_props(player_data, prop_types)
    
    for prop_type, pred in predictions.items():
        print(f"\n{prop_type.title()} Prediction:")
        print(f"Value: {pred['prediction']:.1f}")
        print(f"Confidence: {pred['confidence']:.1%}")
        print("Key Factors:", pred['key_factors'])

def main():
    print("Starting Betting Analyzer Tests...")
    
    # Test live game analysis
    test_live_game_analysis()
    
    # Test player props
    test_player_props()
    
    print("\nAll tests completed!")

if __name__ == "__main__":
    main()
