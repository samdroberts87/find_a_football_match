import requests
import termcolor
import sys


def postcode_validation(max_retries=3):
    postcode_api = "https://api.postcodes.io/postcodes/"
    retries = 0
    while retries < max_retries:
        try:
            postcode = input("Enter your postcode: ").replace(" ", "")
            response = requests.get(f"{postcode_api}{postcode}")
            if response.status_code == 200:
                data = response.json()
                if data["status"] == 200:
                    termcolor.cprint(f"Your postcode has been validated", "green")
                    return postcode  # Return valid postcode
                else:
                    print("Invalid postcode. Please try again.")
            else:
                print("Invalid postcode. Please try again.")
        except requests.RequestException as e:
            print(f"Error occurred: {e}")
            return None
        except (EOFError, KeyboardInterrupt):
            termcolor.cprint("\nUser cancelled program. Exiting...", "red")
            sys.exit(0) 
        retries += 1
    return None  # Return None after max retries
