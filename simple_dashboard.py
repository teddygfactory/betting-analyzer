from dash import Dash, html, dcc, dash_table, Input, Output
import pandas as pd
from betting_analyzer import BettingAnalyzer
import plotly.graph_objs as go

def create_app():
    app = Dash(__name__)
    analyzer = BettingAnalyzer()
    
    app.layout = html.Div(style={'backgroundColor': '#1a1a1a', 'minHeight': '100vh', 'color': 'white', 'padding': '20px'}, children=[
        html.H1('Live Betting Analysis Dashboard', style={'textAlign': 'center', 'color': '#00ff00'}),
        
        # Debug info section
        html.Div(id='debug-info', style={'color': 'yellow', 'margin': '20px 0', 'fontFamily': 'monospace'}),
        
        html.Div([
            # NBA Section
            html.Div([
                html.H2('NBA Betting Opportunities', style={'color': '#ff9900'}),
                dash_table.DataTable(
                    id='nba-table',
                    columns=[
                        {"name": "Time", "id": "time"},
                        {"name": "Matchup", "id": "matchup"},
                        {"name": "Bet Type", "id": "bet_type"},
                        {"name": "Pick", "id": "pick"},
                        {"name": "Odds", "id": "odds"},
                        {"name": "Expected Value", "id": "expected_value"},
                        {"name": "Analysis", "id": "analysis"}
                    ],
                    style_data={
                        'backgroundColor': '#2b2b2b',
                        'color': 'white',
                        'border': '1px solid #404040'
                    },
                    style_header={
                        'backgroundColor': '#404040',
                        'color': 'white',
                        'fontWeight': 'bold',
                        'border': '1px solid #606060'
                    },
                    style_table={'overflowX': 'auto'},
                    page_size=10
                ),
            ], style={'margin': '20px 0'}),
            
            # NFL Section
            html.Div([
                html.H2('NFL Betting Opportunities', style={'color': '#ff9900'}),
                dash_table.DataTable(
                    id='nfl-table',
                    columns=[
                        {"name": "Time", "id": "time"},
                        {"name": "Matchup", "id": "matchup"},
                        {"name": "Bet Type", "id": "bet_type"},
                        {"name": "Pick", "id": "pick"},
                        {"name": "Odds", "id": "odds"},
                        {"name": "Expected Value", "id": "expected_value"},
                        {"name": "Analysis", "id": "analysis"}
                    ],
                    style_data={
                        'backgroundColor': '#2b2b2b',
                        'color': 'white',
                        'border': '1px solid #404040'
                    },
                    style_header={
                        'backgroundColor': '#404040',
                        'color': 'white',
                        'fontWeight': 'bold',
                        'border': '1px solid #606060'
                    },
                    style_table={'overflowX': 'auto'},
                    page_size=10
                ),
            ], style={'margin': '20px 0'}),
            
            # Auto-refresh
            dcc.Interval(
                id='interval-component',
                interval=5*60*1000,  # 5 minutes in milliseconds
                n_intervals=0
            )
        ])
    ])
    
    @app.callback(
        [Output('nba-table', 'data'),
         Output('nfl-table', 'data'),
         Output('debug-info', 'children')],
        Input('interval-component', 'n_intervals')
    )
    def update_tables(_):
        debug_info = []
        try:
            # Get latest betting opportunities
            debug_info.append("Fetching best bets...")
            best_bets = analyzer.get_todays_best_bets()
            debug_info.append(f"Got {len(best_bets)} total bets")
            
            # Separate NBA and NFL bets
            nba_bets = [bet for bet in best_bets if bet['sport'] == 'NBA']
            nfl_bets = [bet for bet in best_bets if bet['sport'] == 'NFL']
            debug_info.append(f"NBA bets: {len(nba_bets)}")
            debug_info.append(f"NFL bets: {len(nfl_bets)}")
            
            # Format expected value as percentage
            for bets in [nba_bets, nfl_bets]:
                for bet in bets:
                    bet['expected_value'] = f"{bet['expected_value']:.1f}%"
            
            return nba_bets, nfl_bets, '\n'.join(debug_info)
        except Exception as e:
            debug_info.append(f"Error: {str(e)}")
            return [], [], '\n'.join(debug_info)
    
    return app

if __name__ == '__main__':
    app = create_app()
    print("\nStarting Live Betting Dashboard...")
    print("Access the dashboard at http://localhost:8050")
    print("Press Ctrl+C to stop")
    app.run_server(debug=False, port=8050)
