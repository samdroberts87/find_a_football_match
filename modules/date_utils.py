import time

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
        except EOFError:
            print("\nInput interrupted. Exiting...")
