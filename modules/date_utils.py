import time
import sys
from datetime import datetime, timedelta
import termcolor


def convert_date_format():
    time.sleep(1)
    print("Enter the date you wish to see a match.")
    while True:
        time.sleep(1)
        date = input("Date format must be DD/MM/YYYY: ")
        try:
            if "/" in date:
                day, month, year = date.split("/")
                day = int(day)
                month = int(month)
                year = int(year)

                # Try to create a datetime object
                try:
                    user_date = datetime(year, month, day)
                except ValueError:
                    print("Please pick a real date.")
                    continue  # Retry input

                current_date = datetime.now()

                # Check if the date is in the past
                if user_date < current_date:
                    print("The date cannot be in the past.")
                    raise ValueError

                # Check if the date is more than 5 weeks in the future
                if user_date > current_date + timedelta(days=36):
                    print(
                        "The date is more than 5 weeks in the future. \nWe can only get data for the next 5 weeks."
                    )
                    raise ValueError

                # Return the formatted date
                return f"{year}-{month:02d}-{day:02d}"
            else:
                print("Date format incorrect.")
        except ValueError:
            continue
        except (EOFError, KeyboardInterrupt):
            termcolor.cprint("\nUser cancelled program. Exiting...", "red")
            sys.exit(0)
