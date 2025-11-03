import fastf1 as f1
import pandas as pd
import data
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt

def get_race_data():
    '''
    Retrieve past race lap time data along with 
    tire compound used and its longevity
    '''
    session = f1.get_session(2023, 'Monza', 'R')
    session.load()
    laps = session.laps
    laps['Time'] = (laps['LapStartTime'] - laps['LapStartTime'].iloc[0]).dt.total_seconds()
    laps = laps.dropna(subset=['LapTime', 'LapStartTime'])
    print(laps[['Driver', 'LapTime', 'Compound', 'TyreLife']].head())
    return laps

def combine_data():
    '''
    Merging weather data with lap times based off timestamps
    '''
    weather = data.process_database()
    weather = weather.dropna(subset=['timestamp', 'temp_c'])
    weather['Time'] = (weather['timestamp'] - weather['timestamp'].iloc[0]).dt.total_seconds()
    laps = get_race_data()

    merged_data = pd.merge_asof(
        laps.sort_values('Time'), 
        weather.sort_values('Time'),
        on='Time', 
        direction='nearest')
    
    merged_data = merged_data.dropna(subset=['LapTime', 'temp_c'])
    print(merged_data.head())
    return merged_data

def visualize_data():
    intial_fuel = 100
    fuel_per_lap = 2.5
    merged_data = combine_data()
    merged_data = merged_data.sort_values('Time')
    merged_data['fuel_kg'] = intial_fuel - fuel_per_lap * merged_data.groupby('Driver').cumcount()
    feature_cols = ['temp_c', 'wind_kph', 'humidity', 'precip_mm',
                    'vis_km', 'cloud', 'gust_kph', 'fuel_kg']
    
    merged_data = merged_data.dropna(subset=feature_cols + ['LapTime'])

    X = merged_data[feature_cols]
    y = merged_data['LapTime'].dt.total_seconds()

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    print(f"Model R^2 score: {model.score(X_test, y_test):.2f}")
    
    plt.scatter(merged_data['temp_c'], y)
    plt.xlabel('Temperature (°C)')
    plt.ylabel('Lap Time (s)')
    plt.title('Temperature vs Lap Time')
    plt.show()


def main():
    combine_data()
    visualize_data()

if __name__ == '__main__':
    main()