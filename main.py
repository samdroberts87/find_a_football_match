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
                print("Valid postcode.")
                break  # Exit the loop once a valid postcode is entered
            else:
                print("Invalid postcode. Please try again.")
    except EOFError:  # Handle Ctrl+D (End of Input)
        print("\nInput interrupted. Exiting...")
    date_of_match = convert_date_format()
    print(date_of_match)


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


def convert_date_format():

    print("Enter the date you wish to see a match")
    while True:
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


if __name__ == "__main__":
    main()
