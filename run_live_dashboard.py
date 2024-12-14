from betting_analyzer import BettingAnalyzer
from advanced_visualization import LiveDashboardManager, VisualizationConfig
from dash import Input, Output
import pandas as pd

def main():
    # Initialize analyzer and dashboard
    analyzer = BettingAnalyzer()
    config = VisualizationConfig(
        title='Live Betting Analysis Dashboard',
        dark_mode=True,
        refresh_interval=300  # 5 minutes
    )
    dashboard = LiveDashboardManager(config)
    
    # Set up data callback
    @dashboard.app.callback(
        [Output('upcoming-games-table', 'data'),
         Output('best-bets-table', 'data')],
        Input('interval-component', 'n_intervals')
    )
    def update_data(_):
        # Get latest bets
        best_bets = analyzer.get_todays_best_bets()
        
        # Convert to DataFrame for display
        bets_df = pd.DataFrame(best_bets)
        
        # Update games table
        games = bets_df[['sport', 'time', 'matchup']].drop_duplicates()
        games_data = games.to_dict('records')
        
        # Update bets table
        bets_data = bets_df[['sport', 'time', 'matchup', 'bet_type', 'pick', 'odds', 'expected_value', 'analysis']].to_dict('records')
        
        return games_data, bets_data
    
    # Run the dashboard
    print("\nStarting Live Betting Dashboard...")
    print("Access the dashboard at http://localhost:8050")
    print("Press Ctrl+C to stop")
    
    dashboard.app.run(debug=False, port=8050)

if __name__ == "__main__":
    main()
