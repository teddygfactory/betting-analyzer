from http.server import BaseHTTPRequestHandler
from betting.analyzer import BettingAnalyzer
import json

def handler(event, context):
    try:
        analyzer = BettingAnalyzer()
        best_bets = analyzer.get_todays_best_bets()
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'bets': best_bets
            })
        }
    except Exception as e:
        print(f"Error in API handler: {str(e)}")  
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': str(e)
            })
        }
