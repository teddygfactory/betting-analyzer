from betting_analyzer import BettingAnalyzer

def main():
    analyzer = BettingAnalyzer()
    best_bets = analyzer.get_best_bets_today()
    
    print("\nBest Betting Opportunities Today:")
    print("=================================")
    
    for bet in best_bets[:5]:  # Show top 5 bets
        print(f"\n{bet['sport']} - {bet['time']}")
        print(f"Matchup: {bet['matchup']}")
        print(f"Bet Type: {bet['bet_type']}")
        print(f"Pick: {bet['pick']} ({bet['odds']})")
        print(f"Analysis: {bet['analysis']}")
        print("Confidence: {:.1%}".format(bet['confidence']))

if __name__ == "__main__":
    main()
