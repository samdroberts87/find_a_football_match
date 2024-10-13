import requests
import time
from geopy.geocoders import Nominatim
from geopy.distance import great_circle

premier_league_teams = {
    "liverpool": "L4 0TH",                     # Anfield
    "manchester city": "M11 3FF",              # Etihad Stadium
    "arsenal": "N5 1BU",                        # Emirates Stadium
    "chelsea": "SW6 1HS",                       # Stamford Bridge
    "aston villa": "B6 6HE",                    # Villa Park
    "brighton and hove albion": "BN1 9BL",     # Amex Stadium
    "newcastle united": "NE1 4ST",              # St James' Park
    "fulham": "SW6 6HH",                        # Craven Cottage
    "tottenham hotspur": "N17 0AP",             # Tottenham Hotspur Stadium
    "nottingham forest": "NG2 3HN",             # City Ground
    "brentford": "TW8 0NT",                     # Gtech Community Stadium
    "west ham united": "E20 2ST",               # London Stadium
    "bournemouth": "BH7 7AF",                   # Vitality Stadium
    "manchester united": "M16 0RA",             # Old Trafford
    "leicester city": "LE2 7FL",                # King Power Stadium
    "everton": "L4 4EL",                        # Goodison Park
    "ipswich": "IP1 2DA",                       # Portman Road
    "crystal palace": "SE25 6PU",               # Selhurst Park
    "southampton": "SO14 5FP",                  # St Mary's Stadium
    "wolverhampton wanderers": "WV1 4QR"        # Molineux Stadium
}

# Initialize the geocoder
geolocator = Nominatim(user_agent="postcode_distance_checker")

def main():
    print("Welcome to Find A Football Match")
    time.sleep(1)
    print("Let's find you a premier league football match to watch!")
    try:
        while True:
            postcode = input("Enter your postcode: ")
            if postcode_validation(postcode):
                print(f"Your postcode has been validated and set at {postcode}.")
                break  # Exit the loop once a valid postcode is entered
            else:
                print("Invalid postcode. Please try again.")
    except EOFError:  # Handle Ctrl+D (End of Input)
        print("\nInput interrupted. Exiting...")

    date_of_match = convert_date_format()
    time.sleep(0.5)
    print(f"Your chosen date is: {date_of_match}")
    distance = get_travel_miles()
    time.sleep(0.5)
    print(f"You are willing to travel: {distance:.2f} miles")
    car_bool = have_car()
    time.sleep(0.5)
    if car_bool:
        print(
            "Okay, so you can travel by car. We'll provide you the Google Maps route."
        )
    else:
        print("Okay, No car - No problem. We'll get you train details.")

    print(
        "Thank you for that information. We'll get right on it. Please wait a few moments...."
    )

    # Find nearby teams
    nearby_teams = find_nearby_postcodes(postcode, distance, premier_league_teams)
    if nearby_teams:
        print("Teams within your travel distance:")
        for team, team_postcode, team_distance in nearby_teams:
            print(f" - {team.title()} ({team_postcode}): {team_distance:.2f} miles")
    else:
        print("No teams found within your travel distance.")

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

def have_car():
    while True:
        time.sleep(1)
        result = input("Do you own a car? (y/n): ").lower()
        try:
            if result not in ["yes", "y", "no", "n"]:
                print("Invalid input. Please enter 'y' or 'n'.")
                continue
            elif result in ["yes", "y"]:
                return True
            elif result in ["no", "n"]:
                return False
        except ValueError:
            print("Invalid input. Please enter 'y' or 'n'.")
        except EOFError:  # Handle Ctrl+D (End of Input)
            print("\nInput interrupted. Exiting...")

def find_nearby_postcodes(target_postcode, distance_limit_miles, teams):
    """Find postcodes within the specified distance from the target postcode."""
    target_coords = get_coordinates(target_postcode)
    if not target_coords:
        return []

    nearby_teams = []

    for team, postcode in teams.items():
        coords = get_coordinates(postcode)
        if coords:
            distance = great_circle(target_coords, coords).miles
            if distance <= distance_limit_miles:
                nearby_teams.append((team, postcode, distance))
    
    return nearby_teams

def get_coordinates(postcode):
    """Get the latitude and longitude of a postcode."""
    location = geolocator.geocode(postcode + ", UK")
    if location:
        return (location.latitude, location.longitude)
    else:
        print(f"Could not find coordinates for postcode: {postcode}")
        return None

if __name__ == "__main__":
    main()
