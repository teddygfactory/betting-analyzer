from betting_analyzer import BettingAnalyzer
import time
import pandas as pd
from datetime import datetime

def main():
    print("Starting Betting Analyzer Dashboard...")
    analyzer = BettingAnalyzer()
    
    # Start the live monitoring dashboard
    print("\nLaunching dashboard at http://localhost:8050")
    print("Press Ctrl+C to stop the dashboard")
    
    try:
        analyzer.start_live_monitoring()
        
        # Keep updating with sample data while running
        while True:
            # Sample game data (you would replace this with real data)
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
            
            # Update analysis
            analyzer.analyze_live_game(game_data)
            
            # Wait before next update
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("\nStopping dashboard...")
        analyzer.stop_live_monitoring()
        print("Dashboard stopped. Thank you for using Betting Analyzer!")

if __name__ == "__main__":
    main()
