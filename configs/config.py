import os
import sys

from dotenv import load_dotenv

base_url = "https://v3.football.api-sports.io"

headers = {
    'x-rapidapi-host': "v3.football.api-sports.io",
    'x-rapidapi-key': os.getenv('RAPIDAPI_KEY', 'your_rapidapi_key_here')
}

#Bot token from discord developer portal
BOT_TOKEN = os.getenv('BOT_TOKEN', 'your_discord_bot_token_here')

footer_icon_url = os.getenv('FOOTER_ICON_URL', 'https://i.imgur.com/JQsILIF.png')
thumbnail_logo = os.getenv('THUMBNAIL_LOGO', 'https://i.imgur.com/ykPOOnv.png')

#Embed Color
embed_color = int(os.getenv('EMBED_COLOR', '5763719'))

# Footer text
footer_text = os.getenv('FOOTER_TEXT', 'Scoring Returns')

# Website link configuration
website_name = os.getenv('WEBSITE_NAME', 'BernKing Blog')
website_url = os.getenv('WEBSITE_URL', 'https://bernking.xyz/')
website_field_name = "Check it out:"

#The amount of games that can a user can be following at once
MAX_SIMULTANEOUS_GAMES = int(os.getenv('MAX_SIMULTANEOUS_GAMES', '3'))

# League IDs from https://dashboard.api-football.com/soccer/ids
# IDs represent current season competitions
important_leagues_str = os.getenv('IMPORTANT_LEAGUES', '5')
IMPORTANT_LEAGUES = [int(id.strip()) for id in important_leagues_str.split(',')] if important_leagues_str else []

# API Rate Limits
# Free: 10 req/min (100/day)
# Pro: 300 req/min (7,500/day) 
# Ultra: 450 req/min (75,000/day)
# Mega: 900 req/min (150,000/day)
# Custom: 1200 req/min (1.5M/day)

# Note: This project uses api-football.com but is not endorsed by or affiliated with them.
# It was chosen purely based on feature set and reliability at time of development.

# Default wait time for the loop in seconds
# Free tier: 120 seconds to stay under 100 requests/day limit
# Other tiers: 45 seconds is optimal
LOOP_WAIT_TIME = int(os.getenv('LOOP_WAIT_TIME', '120'))

# Season configuration (API season year)
SEASON = int(os.getenv('SEASON', '2025'))

from pathlib import Path

def get_executable_dir():
    if getattr(sys, 'frozen', False):
        # When frozen, use the directory where the executable is located
        return os.path.dirname(os.path.realpath(sys.argv[0]))
    
    else:
        # When not frozen, use the script's parent directory
            
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Ensure we always load the .env from the project root/executable dir
ENV_PATH = Path(get_executable_dir()) / ".env"
load_dotenv(dotenv_path=ENV_PATH, override=True)

# Project structure

print("Path: ", get_executable_dir())

PROJECT_ROOT = Path(get_executable_dir())
IMAGES_HELPER_PATH = PROJECT_ROOT / "images_helper_files"
LOGGING_PATH = IMAGES_HELPER_PATH / "Logging"
FIXTURES_PATH = IMAGES_HELPER_PATH / "AllFixtures"
STANDINGS_PATH = IMAGES_HELPER_PATH / "AllStandings"
BANNERS_PATH = IMAGES_HELPER_PATH / "GameBanners"
LEAGUE_STATUS = IMAGES_HELPER_PATH / "League_Status"

VS_PATH = PROJECT_ROOT / "assets" / "images" / "vs.png"
FIXTURES_BY_LEAGUE_PATH = IMAGES_HELPER_PATH / "fixtures_by_league.json"
INFORMATION_PATH = IMAGES_HELPER_PATH / "information.json"
TEAMS_PATH = IMAGES_HELPER_PATH / "teams.json"
LIVE_JSON_PATH = IMAGES_HELPER_PATH / "LiveJson"
LEAGUES_JSON_PATH = PROJECT_ROOT / "assets" / "leagues_available.json"


