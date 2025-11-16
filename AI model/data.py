import requests
import sqlite3
import pandas as pd
from sklearn.preprocessing import StandardScaler
import datetime as dt
from Back_End import api_key as key


def fetch_forecast(location: str) -> pd.DataFrame:
    '''
    Fetches data from weatherapi.com to get the forecast
    weather data for the next 3 days as a json
    '''
    url = "http://api.weatherapi.com/v1/forecast.json"
    today = dt.date.today()
    params = {"key": key.API_KEY,
            "q": location,
            "days": 3,
            "dt": today.isoformat()
            }
    response = requests.get(url, params = params).json()

    hourly_data = []
    retrieval_time = dt.datetime.now()
    
    for hour_data in response["forecast"]["forecastday"][0]["hour"]:
        timestamp = dt.datetime.strptime(hour_data["time"], "%Y-%m-%d %H:%M")
        hourly_data.append({
            "location": location,
            "timestamp": timestamp,
            "retrieval_time": retrieval_time,
            "temp_c": hour_data["temp_c"],
            "wind_kph": hour_data["wind_kph"],
            "wind_dir": hour_data["wind_dir"],
            "humidity": hour_data["humidity"],
            "precip_mm": hour_data["precip_mm"],
            "condition": hour_data["condition"]["text"],
            "vis_km": hour_data["vis_km"],
            "cloud": hour_data["cloud"],
            "gust_kph": hour_data["gust_kph"]
        })

    return pd.DataFrame(hourly_data)

def preprocess_database() -> pd.DataFrame:
    '''
    One-hot encodes data for ML and sends data to SQL database
    '''
    conn = sqlite3.connect(key.DB_FILE)
    dataframe = pd.read_sql("SELECT * FROM weather_forecast", conn)
    conn.close()

    dataframe = pd.get_dummies(dataframe, columns=["condition", "wind_dir", "location"], prefix=["condition", "wind", "location"])

    scaler = StandardScaler()
    numeric_cols = ["temp_c", "wind_kph", "humidity", "precip_mm", "vis_km", "cloud", "gust_kph"]
    dataframe[numeric_cols] = scaler.fit_transform(dataframe[numeric_cols])
    
    return dataframe

def log_to_database(dataframe: pd.DataFrame):
    '''
    writes weather data into database
    '''
    conn = sqlite3.connect(key.DB_FILE)
    dataframe.to_sql("weather_forecast", conn, if_exists="append", index=False)
    conn.close()


def main():
    locations = ["Monaco", "Silverstone", "Monza", "Spa", "Suzuka"]
    for loc in locations:
        dataframe = fetch_forecast(loc)
        log_to_database(dataframe)
    print("Crontab at", dt.datetime.now())

if __name__ == "__main__":
    main()