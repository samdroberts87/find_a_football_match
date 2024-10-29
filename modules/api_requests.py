import requests
import sys
from modules.config import SPORT_HIGHLIGHTS_API_KEY


def get_fixtures(date_of_match):
    url = "https://sport-highlights-api.p.rapidapi.com/football/matches"
    querystring = {
        "leagueId": "33973",  # Premier League ID
        "season": "2024",
        "date": date_of_match,
    }

    headers = {
        "x-rapidapi-key": SPORT_HIGHLIGHTS_API_KEY,
        "x-rapidapi-host": "sport-highlights-api.p.rapidapi.com",
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        if response.status_code == 200:
            json_data = response.json()
            home_team_names = [match["homeTeam"]["name"] for match in json_data["data"]]
            return home_team_names
        else:
            print(f"Error fetching fixtures. Status Code: {response.status_code}")
            return []
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return []
    except EOFError:
        print("\nInput interrupted. Exiting...")
        sys.exit(0)
    except KeyboardInterrupt:
        termcolor.cprint("EXITING DUE TO USER INTERRUPTION", "red")
        sys.exit(0)   
