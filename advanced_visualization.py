from dash import Dash, html, dcc, dash_table, Input, Output
import plotly.graph_objs as go
import pandas as pd
from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class VisualizationConfig:
    title: str = 'Betting Analysis Dashboard'
    dark_mode: bool = True
    refresh_interval: int = 300  # 5 minutes

class LiveDashboardManager:
    def __init__(self, config: VisualizationConfig):
        self.app = Dash(__name__)
        self.config = config
        self.data_buffer = {
            'upcoming_games': pd.DataFrame(),
            'best_bets': pd.DataFrame(),
            'game_predictions': pd.DataFrame()
        }
        
        # Layout setup
        self.app.layout = html.Div([
            html.H1(config.title, className='dashboard-title'),
            
            # Upcoming Games Section
            html.Div([
                html.H2("Upcoming Games"),
                dash_table.DataTable(
                    id='upcoming-games-table',
                    columns=[
                        {"name": "Time", "id": "Time"},
                        {"name": "Home", "id": "Home"},
                        {"name": "Away", "id": "Away"},
                        {"name": "Spread", "id": "Spread"},
                        {"name": "Total", "id": "Total"},
                        {"name": "ML", "id": "ML"}
                    ],
                    data=[],
                    style_table={'overflowX': 'auto'},
                    style_cell={
                        'textAlign': 'left',
                        'padding': '10px',
                        'backgroundColor': '#2b2b2b' if config.dark_mode else 'white',
                        'color': 'white' if config.dark_mode else 'black'
                    },
                    style_header={
                        'backgroundColor': '#1a1a1a' if config.dark_mode else '#f8f9fa',
                        'fontWeight': 'bold',
                        'color': 'white' if config.dark_mode else 'black'
                    }
                )
            ], className='dashboard-section'),
            
            # Best Bets Section
            html.Div([
                html.H2("Best Bets"),
                dash_table.DataTable(
                    id='best-bets-table',
                    columns=[
                        {"name": "Game", "id": "Game"},
                        {"name": "Bet Type", "id": "BetType"},
                        {"name": "Line", "id": "Line"},
                        {"name": "Odds", "id": "Odds"},
                        {"name": "Value", "id": "Value"}
                    ],
                    data=[],
                    style_table={'overflowX': 'auto'},
                    style_cell={
                        'textAlign': 'left',
                        'padding': '10px',
                        'backgroundColor': '#2b2b2b' if config.dark_mode else 'white',
                        'color': 'white' if config.dark_mode else 'black'
                    },
                    style_header={
                        'backgroundColor': '#1a1a1a' if config.dark_mode else '#f8f9fa',
                        'fontWeight': 'bold',
                        'color': 'white' if config.dark_mode else 'black'
                    }
                )
            ], className='dashboard-section'),
            
            # Predictions Section
            html.Div([
                html.H2("Game Predictions"),
                dcc.Graph(id='predictions-graph')
            ], className='dashboard-section'),
            
            dcc.Interval(
                id='interval-component',
                interval=config.refresh_interval * 1000,  # Convert to milliseconds
                n_intervals=0
            )
        ], className='dashboard-container')
        
        self._setup_callbacks()
    
    def _setup_callbacks(self):
        @self.app.callback(
            [Output('upcoming-games-table', 'data'),
             Output('best-bets-table', 'data'),
             Output('predictions-graph', 'figure')],
            [Input('interval-component', 'n_intervals')]
        )
        def update_tables(n):
            # Upcoming Games
            upcoming_games_data = self.data_buffer['upcoming_games'].to_dict('records')
            
            # Best Bets
            best_bets_data = self.data_buffer['best_bets'].to_dict('records')
            
            # Create predictions graph
            predictions_data = self.data_buffer['game_predictions']
            predictions_graph = {
                'data': [{
                    'x': predictions_data['Game'].tolist() if not predictions_data.empty else [],
                    'y': predictions_data['Prediction'].tolist() if not predictions_data.empty else [],
                    'type': 'bar',
                    'name': 'Win Probability'
                }],
                'layout': {
                    'title': 'Game Predictions',
                    'xaxis': {'title': 'Game'},
                    'yaxis': {'title': 'Win Probability'},
                    'plot_bgcolor': '#2b2b2b' if self.config.dark_mode else 'white',
                    'paper_bgcolor': '#2b2b2b' if self.config.dark_mode else 'white',
                    'font': {'color': 'white' if self.config.dark_mode else 'black'}
                }
            }
            
            return upcoming_games_data, best_bets_data, predictions_graph
    
    def update_all_visualizations(self, data: Dict[str, pd.DataFrame]):
        """Update all visualizations with new data"""
        print("Updating visualizations with data:")
        for key, df in data.items():
            print(f"{key}: {len(df)} rows")
            self.data_buffer[key] = df
    
    def start_dashboard(self):
        """Start the Dash server"""
        print("Starting dashboard server...")
        self.app.run_server(debug=True, port=8050)
    
    def stop_dashboard(self):
        """Stop the Dash server"""
        print("Stopping dashboard server...")
