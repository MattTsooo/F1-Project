from typing import Dict
import requests
import sqlite3
import pandas as pd
from sklearn.preprocessing import StandardScaler
from datetime import datetime


def get_weather() -> Dict:
    '''
    Fetches data from weatherapi.com to get current time
    weather data as a json
    '''
    url = "http://api.weatherapi.com/v1/current.json"
    params = {"key": "b6b414bda24544b3ac5184659250111", 
            "q": "Monaco"
            }
    response = requests.get(url, params = params)
    data = response.json()
    return data

def process_database():
    '''
    Filters weather data to include only relevant information
    Create a database table 
    '''
    data = get_weather()
    current = data["current"]
    weather_queries = {"temp_c": current["temp_c"], "wind_kph": current["wind_kph"],
                    "wind_dir": current["wind_dir"], "humidity": current["humidity"], 
                    "precip_mm": current["precip_mm"], "condition": current["condition"]["text"],
                    "vis_km": current["vis_km"], "cloud": current["cloud"], 
                    "gust_kph": current["gust_kph"], "timestamp": datetime.now()}
    
    dataframe = pd.DataFrame([weather_queries])
    conn = sqlite3.connect("weather.db")
    dataframe.to_sql("weather_data", conn, if_exists='append', index = False)
    conn.close()

    dataframe = pd.get_dummies(dataframe, columns=["condition", "wind_dir"], prefix=["condition", "wind"])
    scaler = StandardScaler()
    numeric_cols = ["temp_c", "wind_kph", "humidity", "precip_mm", "vis_km", "cloud", "gust_kph"]
    dataframe[numeric_cols] = scaler.fit_transform(dataframe[numeric_cols])
    return dataframe

def write_to_csv() -> None:
    dataframe = process_database()
    dataframe['timestamp'] = datetime.now().isoformat()

    try:
        dataframe.to_csv('weather_data.csv', mode='a', index=False, header=False)
    except FileNotFoundError:
        dataframe.to_csv('weather_data.csv', mode='w', index=False, header=True)


def main():
    dataframe = process_database()
    print(dataframe.head())

if __name__ == "__main__":
    main()