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


if __name__ == "__main__":
    main()
