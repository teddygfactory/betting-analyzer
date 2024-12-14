from data_fetchers.hardrock_fetcher import HardRockFetcher
import pandas as pd
import time

def test_live_games():
    print("\nTesting Live Games Fetching...")
    fetcher = HardRockFetcher()
    
    try:
        games = fetcher.get_live_games()
        if not games.empty:
            print("\nLive Games Found:")
            print("=" * 100)
            print(games.to_string())
        else:
            print("No live games found")
    except Exception as e:
        print(f"Error fetching live games: {e}")

def test_player_props():
    print("\nTesting Player Props Fetching...")
    fetcher = HardRockFetcher()
    
    try:
        props = fetcher.get_player_props()
        if not props.empty:
            print("\nPlayer Props Found:")
            print("=" * 100)
            print(props.to_string())
        else:
            print("No player props found")
    except Exception as e:
        print(f"Error fetching player props: {e}")

def test_continuous_updates():
    print("\nTesting Continuous Updates (30 seconds)...")
    fetcher = HardRockFetcher()
    start_time = time.time()
    update_count = 0
    
    try:
        while time.time() - start_time < 30:  # Run for 30 seconds
            print(f"\nUpdate #{update_count + 1}")
            print("=" * 50)
            
            # Get live games
            games = fetcher.get_live_games()
            if not games.empty:
                print("\nLive Games:")
                print(games[['Time', 'Home', 'Away', 'Score']].to_string())  # Show subset of columns
            
            update_count += 1
            time.sleep(5)  # Wait 5 seconds between updates
            
    except KeyboardInterrupt:
        print("\nTest stopped by user")
    except Exception as e:
        print(f"Error during continuous testing: {e}")
    
    print(f"\nCompleted {update_count} updates")

if __name__ == "__main__":
    print("Starting Hard Rock Fetcher Tests...")
    
    # Test individual components
    test_live_games()
    test_player_props()
    
    # Test continuous updates
    test_continuous_updates()
    
    print("\nAll tests completed!")
