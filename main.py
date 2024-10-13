import requests
import time
from geopy.geocoders import Nominatim
from geopy.distance import great_circle
from config import SPORT_HIGHLIGHTS_API_KEY
import sys
import termcolor

premier_league_teams = {
    "Liverpool": ["L40TH", "https://www.liverpoolfc.com/tickets/tickets-availability"],  # Anfield
    "Manchester City": ["M113FF", "https://www.mancity.com/tickets/mens"],  # Etihad Stadium
    "Arsenal": ["N51BU", "https://www.arsenal.com/tickets"],  # Emirates Stadium
    "Chelsea": ["SW61HS", "https://www.chelseafc.com/en/ticket-information"],  # Stamford Bridge
    "Aston Villa": ["B66HE", "https://www.avfc.co.uk/fans/fans-charter/ticketing/"],  # Villa Park
    "Brighton": ["BN19BL", "https://tickets.brightonandhovealbion.com/"],  # Amex Stadium
    "Newcastle": ["NE14ST", "https://tickets.manutd.com/"],  # St James' Park
    "Fulham": ["SW66HH", "https://www.fulhamfc.com/tickets-and-hospitality"],  # Craven Cottage
    "Tottenham": ["N170AP", "https://www.tottenhamhotspur.com/tickets"],  # Tottenham Hotspur Stadium
    "Nottingham Forest": ["NG25FJ", "https://www.eticketing.co.uk/nottinghamforest"],  # City Ground
    "Brentford": ["TW80NT", "https://www.eticketing.co.uk/brentfordfc"],  # Gtech Community Stadium
    "West Ham": ["E202ST", "https://www.eticketing.co.uk/whufc"],  # London Stadium
    "Bournemouth": ["BH77AF", "https://www.afcb.co.uk/tickets/"],  # Vitality Stadium
    "Manchester United": ["M160RA", "https://www.manutd.com/tickets"],  # Old Trafford
    "Leicester": ["LE27FL", "https://www.premierleague.com/www.lcfc.com/season-tickets"],  # King Power Stadium
    "Everton": ["L44EL", "https://www.evertonfc.com/tickets/latest"],  # Goodison Park
    "Ipswich": ["IP12DA", "https://tickets.itfc.co.uk/"],  # Portman Road
    "Crystal Palace": ["SE256PU", "https://www.eticketing.co.uk/cpfc/"],  # Selhurst Park
    "Southampton": ["SO145FP", "https://www.premierleague.com/southamptonfc.com/match-tickets"],  # St Mary's Stadium
    "Wolves": ["WV14QR", "https://www.eticketing.co.uk/wolves"]  # Molineux Stadium
}

# Initialize the geocoder
geolocator = Nominatim(user_agent="postcode_distance_checker")


def main():
    termcolor.cprint("\nWelcome to Find A Football Match", "green")
    time.sleep(1)
    print("Let's find you a premier league football match to watch!")
    try:
        while True:
            postcode = input("Enter your postcode: ").replace(" ", "")
            if postcode_validation(postcode):
                termcolor.cprint(f"Your postcode has been validated and set as {postcode}", "green")
                break  # Exit the loop once a valid postcode is entered
            else:
                print("Invalid postcode. Please try again.")
    except EOFError:  # Handle Ctrl+D (End of Input)
        print("\nInput interrupted. Exiting...")

    date_of_match = convert_date_format()
    time.sleep(0.5)
    termcolor.cprint(f"Your chosen date is: {date_of_match}", "green")
    distance = get_travel_miles()
    time.sleep(0.5)
    termcolor.cprint(f"You are willing to travel: {distance:.2f} miles", "green")
    termcolor.cprint(
        "Please wait a few moments....", attrs=["bold"] 
    )
    # Find nearby teams
    nearby_teams = find_nearby_postcodes(postcode, distance, premier_league_teams)
    if nearby_teams:
        termcolor.cprint("Teams within your travel distance:", "green")
        for team, team_postcode, team_distance in nearby_teams:
            print(f" - {team.title()} ({team_postcode}): {team_distance:.2f} miles")
    else:
        termcolor.cprint("No teams found within your travel distance.", "red")
        sys.exit(0)

    time.sleep(1)
    print(f"Let's see which of those teams are playing at home on {date_of_match}\n")

    home_teams = get_fixtures(date_of_match)

    available_teams = []
    for team, _, _ in nearby_teams:
        if team in home_teams:
            available_teams.append(team)

    if not available_teams:
        termcolor.cprint(
            f"Sorry, no matches available on {date_of_match} within {distance} miles of {postcode}", "red"
        )
    else:
        for i in available_teams:
            time.sleep(0.5)
            url = f"https://www.google.com/maps/dir/{postcode}/{premier_league_teams[i][0]}"
            termcolor.cprint(f"{i} are at home", "green", attrs=["bold"])
            print(f"Here's the club's website to buy tickets: {premier_league_teams[i][1]}")
            print(f"Here's a google maps link with details of how to get there: {url}")




def postcode_validation(postcode):
    try:
        postcode_api = "https://api.postcodes.io/postcodes/"
        response = requests.get(f"{postcode_api}{postcode}")

        if response.status_code == 200:
            data = response.json()
            return data["status"] == 200  # Return True if valid postcode
        else:
            return False  # Invalid postcode
    except requests.RequestException as e:
        print(f"Error occurred: {e}")
        return False  # Return False if there's an error during the request
    except EOFError:  # Handle Ctrl+D (End of Input)
        print("\nInput interrupted. Exiting...")


def convert_date_format():
    time.sleep(1)
    print("Enter the date you wish to see a match")
    while True:
        time.sleep(1)
        date = input("Date format must be DD/MM/YYYY: ")
        try:
            if "/" in date:
                day, month, year = date.split("/")
                day = int(day)
                month = int(month)
                year = int(year)
                if day > 31 or month > 12 or year < 2024:
                    raise ValueError
                return f"{year}-{month:02d}-{day:02d}"
            else:
                print("Date format incorrect.")
        except ValueError:
            continue
        except EOFError:  # Handle Ctrl+D (End of Input)
            print("\nInput interrupted. Exiting...")


def get_travel_miles():
    while True:
        time.sleep(1)
        miles = input("Enter the number of miles you are willing to travel: ")
        try:
            miles = float(miles)  # Convert to float
            if miles < 0:  # Check for negative values
                print("Invalid input. Please enter a non-negative number.")
                continue
            return miles
        except ValueError:
            print("Invalid input. Please enter a number.")
        except EOFError:  # Handle Ctrl+D (End of Input)
            print("\nInput interrupted. Exiting...")


def find_nearby_postcodes(target_postcode, distance_limit_miles, teams):
    try:
        target_coords = get_coordinates(target_postcode)
        if not target_coords:
            return []

        nearby_teams = []

        for team, team_data in teams.items():
            postcode = team_data[0]  # Extract the postcode from the list
            coords = get_coordinates(postcode)
            if coords:
                distance = great_circle(target_coords, coords).miles
                if distance <= distance_limit_miles:
                    nearby_teams.append((team, postcode, distance))

        return nearby_teams
    except EOFError:  # Handle Ctrl+D (End of Input)
        print("\nInput interrupted. Exiting...")



def get_coordinates(postcode):
    """Get the latitude and longitude of a postcode."""
    try:
        location = geolocator.geocode(postcode + ", UK")
        if location:
            return (location.latitude, location.longitude)
        else:
            print(f"Could not find coordinates for postcode: {postcode}")
            return None
    except EOFError:  # Handle Ctrl+D (End of Input)
        print("\nInput interrupted. Exiting...")


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

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            json_data = response.json()

            # Extract home team names
            home_team_names = [match["homeTeam"]["name"] for match in json_data["data"]]

            return home_team_names
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except EOFError:  # Handle Ctrl+D (End of Input)
        print("\nInput interrupted. Exiting...")


if __name__ == "__main__":
    main()
