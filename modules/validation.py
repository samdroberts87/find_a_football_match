import requests

def postcode_validation(postcode):
    try:
        postcode_api = "https://api.postcodes.io/postcodes/"
        response = requests.get(f"{postcode_api}{postcode}")

        if response.status_code == 200:
            data = response.json()
            return data["status"] == 200  # Return True if valid postcode
        else:
            return False
    except requests.RequestException as e:
        print(f"Error occurred: {e}")
        return False
    except EOFError:
        print("\nInput interrupted. Exiting...")
