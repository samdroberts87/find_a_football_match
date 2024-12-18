import time
import sys
import termcolor
from modules.team_data import premier_league_teams
from modules.validation import postcode_validation
from modules.date_utils import convert_date_format
from modules.geolocation import get_travel_miles, find_nearby_postcodes
from modules.api_requests import get_fixtures


def main():
    try:
        play_again = True
        while play_again:
            termcolor.cprint("\nWelcome to Find A Football Match", "green")
            time.sleep(1)
            print("Let's find you a premier league football match to watch!")

            postcode = postcode_validation()
            if postcode:
                termcolor.cprint(f"{postcode} is now set. Proceeding...", "green")
            else:
                termcolor.cprint(
                    "Exiting program due to an error or user interruption.", "red"
                )
                sys.exit(0)  # Exit the program

            date_of_match = convert_date_format()
            time.sleep(0.5)
            termcolor.cprint(f"Your chosen date is: {date_of_match}", "green")
            distance = get_travel_miles()
            time.sleep(0.5)
            termcolor.cprint(
                f"You are willing to travel: {distance:.2f} miles", "green"
            )
            termcolor.cprint("Please wait a few moments....", attrs=["bold"])

            nearby_teams = find_nearby_postcodes(
                postcode, distance, premier_league_teams
            )

            if nearby_teams:
                termcolor.cprint("Teams within your travel distance:", "green")
                for team, team_postcode, team_distance in nearby_teams:
                    print(
                        f" - {team.title()} ({team_postcode}): {team_distance:.2f} miles"
                    )
            else:
                termcolor.cprint("No teams found within your travel distance.", "red")
                sys.exit(0)

            time.sleep(1)
            print(
                f"Let's see which of those teams are playing at home on {date_of_match}\n"
            )

            home_teams = get_fixtures(date_of_match)
            available_teams = []

            for team, _, _ in nearby_teams:
                if team in home_teams:
                    available_teams.append(team)

            if not available_teams:
                termcolor.cprint(
                    f"Sorry, no matches available on {date_of_match} within {distance} miles of {postcode}",
                    "red",
                )
            else:
                for i in available_teams:
                    time.sleep(0.5)
                    url = f"https://www.google.com/maps/dir/{postcode}/{premier_league_teams[i][0]}"
                    termcolor.cprint(f"{i} are at home", "green", attrs=["bold"])
                    print(f"Buy tickets: {premier_league_teams[i][1]}")
                    print(f"Get there: {url}")

            answer = input(f"\nWant to go again? (Y/N)").lower()
            if answer in ["y", "yes"]:
                play_again = True
                time.sleep(0.5)
                termcolor.cprint("okay, let's go again", attrs=["bold"])
            else:
                termcolor.cprint("Okay, Exiting", "red", attrs=["bold"])
                time.sleep(0.5)
                sys.exit("thank you for using the app")
    except (EOFError, KeyboardInterrupt):
        termcolor.cprint("\nUser cancelled program. Exiting...", "red")
        sys.exit(0)      


if __name__ == "__main__":
    main()
