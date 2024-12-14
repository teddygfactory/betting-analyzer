from flask import Flask, render_template
from betting_analyzer import BettingAnalyzer
import pandas as pd

app = Flask(__name__)
analyzer = BettingAnalyzer()

@app.route('/')
def index():
    best_bets = analyzer.get_todays_best_bets()
    
    # Group bets by sport
    nba_bets = [bet for bet in best_bets if bet['sport'] == 'NBA']
    nfl_bets = [bet for bet in best_bets if bet['sport'] == 'NFL']
    
    return render_template('index.html', 
                         nba_bets=nba_bets, 
                         nfl_bets=nfl_bets)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
