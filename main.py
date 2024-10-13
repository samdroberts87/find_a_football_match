import requests
import time


def main():
    print("Welcome to Find A Football Match")
    time.sleep(1)
    print("Let's find you a football match to watch!")
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
    print(f"You are willing to travel: {distance}")
    car_bool = have_car()
    time.sleep(0.5)
    if car_bool:
        print("Okay, so you can travel by car. We'll get provide you the google maps route.")
    else:
        print("Okay, No car - No problem. We'll get you train details. ")
    print("Thank you for that information. We'll get right on it. Please wait a few moments....")


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
                print("date format incorrect")
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
                print("Invalid input. Please enter a non-negative number.")
                continue
            elif result in ["yes", "y"]:
                result = True
                return result
            elif result in ["no", "n"]:
                result = False
                return result
        except ValueError:
            print("Invalid input. Please enter a number.")
        except EOFError:  # Handle Ctrl+D (End of Input)
            print("\nInput interrupted. Exiting...")


if __name__ == "__main__":
    main()
