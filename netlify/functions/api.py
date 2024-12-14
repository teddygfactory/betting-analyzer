from http.server import BaseHTTPRequestHandler
from betting_analyzer import BettingAnalyzer
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
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }
