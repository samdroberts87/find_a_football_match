import time
import sys
from geopy.geocoders import Nominatim
from geopy.distance import great_circle
import termcolor

geolocator = Nominatim(user_agent="postcode_distance_checker")


def get_travel_miles():
    while True:
        time.sleep(1)
        miles = input("Enter the number of miles you are willing to travel: ")
        try:
            miles = float(miles)
            if miles < 0:
                print("Invalid input. Please enter a non-negative number.")
                continue
            return miles
        except ValueError:
            print("Invalid input. Please enter a number.")
        except (EOFError, KeyboardInterrupt):
            termcolor.cprint("\nUser cancelled program. Exiting...", "red")
            sys.exit(0)


def find_nearby_postcodes(target_postcode, distance_limit_miles, teams):
    try:
        target_coords = get_coordinates(target_postcode)
        if not target_coords:
            return []

        nearby_teams = []
        for team, team_data in teams.items():
            postcode = team_data[0]
            coords = get_coordinates(postcode)
            if coords:
                distance = great_circle(target_coords, coords).miles
                if distance <= distance_limit_miles:
                    nearby_teams.append((team, postcode, distance))
        return nearby_teams
    except (EOFError, KeyboardInterrupt):
        termcolor.cprint("\nUser cancelled program. Exiting...", "red")
        sys.exit(0)


def get_coordinates(postcode):
    try:
        location = geolocator.geocode(postcode + ", UK")
        if location:
            return (location.latitude, location.longitude)
        else:
            print(f"Could not find coordinates for postcode: {postcode}")
            return None
    except (EOFError, KeyboardInterrupt):
        termcolor.cprint("\nUser cancelled program. Exiting...", "red")
        sys.exit(0)
