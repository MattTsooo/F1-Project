import pandas as pd

def simulate_race(model, merged_data, feature_cols, total_laps = 53, initial_fuel = 100, 
                  fuel_per_lap = 2.5, initial_tyre_life = 20, pit_stop_time = 25):
    lap_times = []
    fuel = initial_fuel
    tyre_life = initial_tyre_life

    base_features = merged_data[feature_cols].iloc[-1].to_dict()

    for lap in range(total_laps):
        features = base_features.copy()
        features['fuel_kg'] = fuel

        X_lap = pd.DataFrame([features])
        lap_time = model.predict(X_lap)[0]

        if tyre_life <= 0:
            lap_time += pit_stop_time
            tyre_life = initial_tyre_life

        lap_times.append(lap_time)

        fuel -= fuel_per_lap
        tyre_life -= 1

    total_race_time = sum(lap_times)
    return total_race_time, lap_times


        