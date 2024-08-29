import requests
from datetime import datetime, timedelta

def fetch_data(number, date):
    url = f"https://results.telc.net/api/results/loopkup/{number}/pruefung/{date}/birthdate/2003-07-26"
    print(url)
    response = requests.get(url)
    print(response.status_code)
    if response.status_code == 200:
        return response.json()  # Предположим, что API возвращает JSON
    else:
        return None

def main():
    base_number = 88541
    base_date = "2024-08-02"
    
    # Определение диапазона для чисел и дат
    number_range = range(base_number - 20, base_number + 21)
    print(number_range)
    base_date_obj = datetime.strptime(base_date, "%Y-%m-%d")
    date_range = [(base_date_obj + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(0, 13)]
    print(date_range)
    results = []
    
    for number in number_range:
        for date in date_range:
            data = fetch_data(str(number).zfill(7), date)
            if data:
                print(f"Data found for number: {number}, date: {date}")
                results.append((number, date, data))
    
    # Если нужно сохранить результаты в файл
    with open("results.json", "w") as f:
        import json
        json.dump(results, f, indent=4)

if __name__ == "__main__":
    main()
