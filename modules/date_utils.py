import time
import sys
from datetime import datetime, timedelta


def convert_date_format():
    time.sleep(1)
    print("Enter the date you wish to see a match.")
    time.sleep(0.5)
    print("Cannot be more than 5 weeks (36 days) in the future.")

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
                    print("Please pick a real date.")
                    raise ValueError
                if month in [4, 6, 9, 11] and day > 30:
                    print("There's only 30 days in your selected month.")
                    raise ValueError
                if month == 2:
                    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
                        if day > 29:  # Leap year February
                            print(
                                "There aren't that many days in February, even in a leap year!"
                            )
                            raise ValueError
                    else:
                        if day > 28:  # Non-leap year February
                            print("There are only 28 days in February!")
                            raise ValueError

                user_date = datetime(year, month, day)
                current_date = datetime.now()

                if user_date < current_date:
                    print("The date cannot be in the past.")
                    raise ValueError
                if user_date > current_date + timedelta(days=36):
                    print(
                        "The date is more than 5 weeks in the future. \nWe can only get data for the next 5 weeks"
                    )
                    raise ValueError

                return f"{year}-{month:02d}-{day:02d}"
            else:
                print("Date format incorrect.")
        except ValueError:
            continue
        except EOFError:
            print("\nInput interrupted. Exiting...")
            sys.exit(0)
        except KeyboardInterrupt:
            termcolor.cprint("EXITING DUE TO USER INTERRUPTION", "red")
            sys.exit(0)   
