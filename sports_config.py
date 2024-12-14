NBA_CONFIG = {
    'league_id': 12,  # NBA league ID for API-Sports
    'current_season': 2023,
    'bet_types': [
        'moneyline',
        'spread',
        'totals',
        'player_props'
    ],
    'key_stats': [
        'points',
        'rebounds',
        'assists',
        'field_goal_percentage',
        'three_point_percentage',
        'free_throw_percentage'
    ]
}

NFL_CONFIG = {
    'league_id': 1,  # NFL league ID for API-Sports
    'current_season': 2023,
    'bet_types': [
        'moneyline',
        'spread',
        'totals',
        'player_props'
    ],
    'key_stats': [
        'passing_yards',
        'rushing_yards',
        'touchdowns',
        'interceptions',
        'completion_percentage',
        'third_down_efficiency'
    ]
}

STAT_WEIGHTS = {
    'NBA': {
        'recent_form': 0.3,
        'h2h_history': 0.2,
        'home_away_performance': 0.15,
        'rest_days': 0.1,
        'injuries': 0.15,
        'pace_factor': 0.1
    },
    'NFL': {
        'recent_form': 0.25,
        'h2h_history': 0.2,
        'home_away_performance': 0.15,
        'rest_days': 0.15,
        'injuries': 0.15,
        'weather_conditions': 0.1
    }
}
