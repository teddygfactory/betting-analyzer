import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from typing import Dict, List
import numpy as np

class BettingVisualizer:
    def __init__(self):
        self.style = 'darkgrid'
        self.figsize = (12, 6)
        sns.set_style(self.style)

    def plot_team_trends(self, team_data: pd.DataFrame, metrics: List[str], title: str) -> None:
        """Plot multiple team performance metrics over time"""
        plt.figure(figsize=self.figsize)
        for metric in metrics:
            plt.plot(team_data.index, team_data[metric], label=metric)
        plt.title(title)
        plt.legend()
        plt.show()

    def plot_head_to_head_comparison(self, team1_stats: Dict, team2_stats: Dict, metrics: List[str]) -> None:
        """Create bar plot comparing two teams across multiple metrics"""
        plt.figure(figsize=self.figsize)
        x = np.arange(len(metrics))
        width = 0.35

        plt.bar(x - width/2, [team1_stats[m] for m in metrics], width, label='Team 1')
        plt.bar(x + width/2, [team2_stats[m] for m in metrics], width, label='Team 2')

        plt.xlabel('Metrics')
        plt.ylabel('Values')
        plt.title('Head-to-Head Comparison')
        plt.xticks(x, metrics, rotation=45)
        plt.legend()
        plt.tight_layout()
        plt.show()

    def plot_betting_history(self, betting_history: pd.DataFrame) -> None:
        """Plot betting performance over time"""
        plt.figure(figsize=self.figsize)
        plt.subplot(2, 1, 1)
        plt.plot(betting_history.index, betting_history['cumulative_profit'], label='Cumulative Profit')
        plt.title('Betting Performance')
        plt.legend()

        plt.subplot(2, 1, 2)
        plt.bar(betting_history.index, betting_history['profit_per_bet'], label='Profit per Bet')
        plt.axhline(y=0, color='r', linestyle='-')
        plt.legend()
        plt.tight_layout()
        plt.show()

    def plot_win_probability_distribution(self, probabilities: List[float]) -> None:
        """Plot distribution of win probabilities"""
        plt.figure(figsize=self.figsize)
        sns.histplot(probabilities, bins=20)
        plt.title('Win Probability Distribution')
        plt.xlabel('Probability')
        plt.ylabel('Frequency')
        plt.show()

    def plot_prop_bet_analysis(self, player_stats: Dict, prop_line: float, prop_type: str) -> None:
        """Visualize player prop bet analysis"""
        plt.figure(figsize=self.figsize)
        
        # Historical performance
        historical_values = player_stats.get('historical_values', [])
        plt.subplot(2, 1, 1)
        plt.plot(historical_values, label='Historical Performance')
        plt.axhline(y=prop_line, color='r', linestyle='--', label='Prop Line')
        plt.title(f'{prop_type} Performance History')
        plt.legend()

        # Distribution
        plt.subplot(2, 1, 2)
        sns.histplot(historical_values, bins=20)
        plt.axvline(x=prop_line, color='r', linestyle='--', label='Prop Line')
        plt.title(f'{prop_type} Distribution')
        plt.legend()
        
        plt.tight_layout()
        plt.show()

    def plot_correlation_matrix(self, data: pd.DataFrame, title: str) -> None:
        """Plot correlation matrix of betting factors"""
        plt.figure(figsize=(10, 8))
        correlation_matrix = data.corr()
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
        plt.title(title)
        plt.show()

    def plot_bankroll_evolution(self, bankroll_history: pd.DataFrame) -> None:
        """Plot bankroll evolution over time with key metrics"""
        plt.figure(figsize=self.figsize)
        
        # Bankroll curve
        plt.plot(bankroll_history.index, bankroll_history['balance'], label='Bankroll')
        
        # Add drawdown overlay
        plt.fill_between(bankroll_history.index, 
                        bankroll_history['balance'], 
                        bankroll_history['peak_balance'],
                        alpha=0.3,
                        label='Drawdown')
        
        plt.title('Bankroll Evolution')
        plt.xlabel('Date')
        plt.ylabel('Balance')
        plt.legend()
        plt.grid(True)
        plt.show()

    def plot_bet_type_performance(self, performance_data: Dict) -> None:
        """Plot performance by bet type"""
        plt.figure(figsize=self.figsize)
        
        bet_types = list(performance_data.keys())
        win_rates = [data['win_rate'] for data in performance_data.values()]
        roi = [data['roi'] for data in performance_data.values()]
        
        x = np.arange(len(bet_types))
        width = 0.35
        
        plt.bar(x - width/2, win_rates, width, label='Win Rate')
        plt.bar(x + width/2, roi, width, label='ROI')
        
        plt.xlabel('Bet Type')
        plt.ylabel('Percentage')
        plt.title('Performance by Bet Type')
        plt.xticks(x, bet_types, rotation=45)
        plt.legend()
        plt.tight_layout()
        plt.show()
