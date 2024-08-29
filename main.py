import requests
from datetime import datetime, timedelta
import argparse


def fetch_data(number, date, birthday):
    url = f"https://results.telc.net/api/results/loopkup/{number}/pruefung/{date}/birthdate/{birthday}"
    print(url)
    response = requests.get(url)
    print(response.status_code)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def main(base_number, base_date, number_range_offset, date_range_offset, birthday):
    intbase_number = int(base_number)
    number_range = range(intbase_number - number_range_offset, intbase_number + number_range_offset)
    print(number_range)
    base_date_obj = datetime.strptime(base_date, "%Y-%m-%d")
    date_range = [(base_date_obj + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(0, date_range_offset)]
    print(date_range)
    results = []
    
    for number in number_range:
        format_number = str(number).zfill(len(str(base_number)))
        for date in date_range:
            data = fetch_data(format_number, date, birthday)
            if data:
                print(f"Data found for number: {number}, date: {date}")
                results.append((number, date, data))
                with open("results.json", "w") as f:
                    import json
                    json.dump(results, f, indent=4)
                return
    print(f"Data not found")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse and fetch data from telc results API")
    
    parser.add_argument("birthday", type=str, help="Your birthday date for the query in YYYY-MM-DD format (e.g., 2000-02-22)")
    parser.add_argument("base_number", type=str, help="Number of the known member for the query (e.g., 0088541)")
    parser.add_argument("number_range_offset", type=int, help="Offset range for number (e.g., 20 for -20 to +20)")
    parser.add_argument("base_date", type=str, help="Day of your exam for the query in YYYY-MM-DD format (e.g., 2024-08-02)")
    parser.add_argument("date_range_offset", type=int, help="Positiv offset range for exam date (e.g., 14 for 14 days after exam)")

    args = parser.parse_args()
    
    main(args.base_number, args.base_date, args.number_range_offset, args.date_range_offset, args.birthday)
