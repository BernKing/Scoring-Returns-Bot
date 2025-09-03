import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import requests
import json
from time import sleep, time
from configs.config import base_url, headers, IMPORTANT_LEAGUES, LEAGUE_STATUS, FIXTURES_PATH, STANDINGS_PATH, SEASON
from scripts.setup_directories import get_executable_dir

def get_league_status(temp_dir=None, season: int = None):
    """
    Fetches current league status data from API and saves to JSON.
    
    Makes GET request to /leagues endpoint with:
    - season: <configured or provided>
    - current: true
    Parameters:
    - temp_dir (Path): Optional temporary directory for GUI mode
    
    Saves response to:
    {LEAGUE_STATUS}/league_status.json
    """
    season = season if season is not None else SEASON
    params = {'season': season, 'current': "true"}
    fixtures_url = base_url + "/leagues"
    response = requests.get(fixtures_url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        # Handle empty responses to surface plan/season issues
        if not data or ('response' in data and len(data.get('response', [])) == 0):
            msg = (
                f"No leagues returned for season {season}. If you're on the free API plan, "
                "try setting SEASON=2023 in your .env or select 2023 in the GUI."
            )
            print(f"⚠️ {msg}")
            # Still save the empty payload for transparency
        file_name = (temp_dir / "league_status.json") if temp_dir else (LEAGUE_STATUS / "league_status.json")
        print(f"Saving league status to: {file_name.absolute()}")
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
        print("League status fetched successfully.")
    else:
        print(f"Error fetching league status: {response.status_code}")
        hint = (
            "Your API key/plan may not allow the selected season. "
        )
        raise Exception(f"API request failed with status code {response.status_code}. {hint}")

def parse_status_fixtures_available():
    """
    Parses league status JSON to find leagues with available fixture statistics.
    
    Reads from:
    {LEAGUE_STATUS}/league_status.json
    
    Returns:
    - list: Tuples of (league_id, league_name) for leagues with stats
    """
    stats_availables = []
    file_name = LEAGUE_STATUS / "league_status.json"
    
    with open(file_name, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
        for league in data["response"]:
            # print(league)
            
            # Loop through each season in the league's "seasons" list
            for season in league["seasons"]:
                # Check if statistics for fixtures are available for this season
                if season["coverage"]["fixtures"]["statistics_fixtures"]:
                    # Append the league ID and name to the stats_availables list
                    stats_availables.append((league['league']['id'], league['league']['name']))
        

                    
    return stats_availables

def get_fixtures_file(stats_availables, important_league, season: int = None):
    """
    Downloads fixture data for specified leagues and saves to JSON files.
    
    Parameters:
    - stats_availables (list): List of (league_id, league_name) tuples
    - important_league (list): List of league IDs to process
    
    Makes GET requests to /fixtures endpoint for each league.
    Saves responses to:
    {FIXTURES_PATH}/{league_id}{league_name}.json
    """
    print("\nFetching Fixtures...")
    for league in stats_availables:
        league_id, league_name = league
      
        if int(league_id) not in important_league:
            continue      

        use_season = season if season is not None else SEASON
        params = {'league': league_id, 'season': use_season, 'timezone' : "Europe/London"}
        fixtures_url = base_url + "/fixtures"
        response = requests.get(fixtures_url, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            file_path = FIXTURES_PATH / f"{league_id}{league_name}.json"
            print(f"Saving fixtures to: {file_path.absolute()}")
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(f"Saved fixtures for {league_name}.")
        else:
            print(f"Error fetching fixtures for {league_name}: {response.status_code}")

def get_league_standings(stats_availables, important_league, season: int = None):
    """
    Downloads standings data for specified leagues and saves to JSON files.
    
    Parameters:
    - stats_availables (list): List of (league_id, league_name) tuples
    - important_league (list): List of league IDs to process
    
    Makes GET requests to /standings endpoint for each league.
    Saves responses to:
    {STANDINGS_PATH}/{league_id}{league_name}.json
    """
    print("\nFetching Standings...")
    for league in stats_availables:
        league_id, league_name = league
        
        if int(league_id) not in important_league:
            continue    
             
        use_season = season if season is not None else SEASON
        params = {'league': league_id, 'season': use_season}
        standings_url = base_url + "/standings"
        response = requests.get(standings_url, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            file_name = STANDINGS_PATH / f"{league_id}{league_name}.json"
            print(f"Saving standings to: {file_name.absolute()}")
            with open(file_name, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(f"Saved standings for {league_name}.")
        else:
            print(f"Error fetching standings for {league_name}: {response.status_code}")
    
    print("\nAll data fetched successfully.")

if __name__ == "__main__":
    
    print(f"\nSaving data to:")
    print(f"League Status: {LEAGUE_STATUS.absolute()}")
    print(f"Fixtures: {FIXTURES_PATH.absolute()}")
    print(f"Standings: {STANDINGS_PATH.absolute()}\n")
    
    get_league_status(season=SEASON)
    stats_availables = parse_status_fixtures_available()
    important_league = IMPORTANT_LEAGUES

    get_fixtures_file(stats_availables, important_league, season=SEASON)
    get_league_standings(stats_availables, important_league, season=SEASON)
    print("\nAll data fetched successfully.")
