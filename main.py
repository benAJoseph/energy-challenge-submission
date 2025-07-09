import pandas as pd
from datetime import datetime
from tariff import get_tariff

# Compute full-load motor power in kW
def calculate_motor_rating():
    equipment_rating = 90  # kW
    efficiency = 0.9
    return equipment_rating / efficiency

# Classify power reading into motor operating states
def classify_power(total_power_kw, motor_rating, service_factor):
    vampire_threshold = 0.01 * motor_rating
    idle_threshold = 0.3 * motor_rating
    overload_threshold = service_factor * motor_rating

    if 0 < total_power_kw <= vampire_threshold:
        return 'vampire'
    elif vampire_threshold < total_power_kw <= idle_threshold:
        return 'idle'
    elif idle_threshold < total_power_kw <= overload_threshold:
        return 'normal'
    elif total_power_kw > overload_threshold:
        return 'overload'
    else:
        return 'unknown'

# Convert timestamp to total minutes since midnight
def parse_time_to_minutes(time_str):
    dt = datetime.fromisoformat(time_str.replace('+00', '+00:00'))
    return dt.hour * 60 + dt.minute

# Return tariff rate in paise/kWh based on hour
def get_tariff_rate(time_str):
    dt = datetime.fromisoformat(time_str.replace('+00', '+00:00'))
    hour = dt.hour

    if 6 <= hour < 18:
        return 790
    elif 18 <= hour < 22:
        return 1185
    else:
        return 593

# Format timestamp as HH:MM
def format_time(time_str):
    dt = datetime.fromisoformat(time_str.replace('+00', '+00:00'))
    return f"{dt.hour:02d}:{dt.minute:02d}"

# Find continuous periods for specific motor states
def find_continuous_periods(df, condition_column):
    periods = {'vampire': [], 'idle': [], 'overload': []}
    
    if df.empty:
        return periods

    current_condition = None
    start_time = None

    for i, row in df.iterrows():
        condition = row[condition_column]

        if condition != current_condition:
            if current_condition in periods and start_time is not None:
                end_time = df.iloc[i-1]['time'] if i > 0 else row['time']
                periods[current_condition].append((format_time(start_time), format_time(end_time)))
            if condition in periods:
                current_condition = condition
                start_time = row['time']
            else:
                current_condition = None
                start_time = None

    if current_condition in periods and start_time is not None:
        end_time = df.iloc[-1]['time']
        periods[current_condition].append((format_time(start_time), format_time(end_time)))

    return periods

# Challenge 1: Calculate energy used by condition
def challenge_1():
    motor_rating = calculate_motor_rating()
    service_factor = 1.2

    df = pd.read_csv('energy.csv')
    df.columns = df.columns.str.strip()
    df['total_power_kw'] = (df['p1'] + df['p2'] + df['p3']) / 1000
    df['condition'] = df['total_power_kw'].apply(
        lambda x: classify_power(x, motor_rating, service_factor)
    )

    energy_consumption = {}
    for condition in ['vampire', 'idle', 'normal', 'overload']:
        condition_energy_wh = df[df['condition'] == condition]['energy'].sum()
        energy_consumption[condition] = int(condition_energy_wh / 1000)

    return energy_consumption

# Challenge 2: Get time ranges for each tracked state
def challenge_2():
    motor_rating = calculate_motor_rating()
    service_factor = 1.2

    df = pd.read_csv('power.csv')
    df.columns = df.columns.str.strip()
    df['total_power_kw'] = (df['p1'] + df['p2'] + df['p3']) / 1000
    df['condition'] = df['total_power_kw'].apply(
        lambda x: classify_power(x, motor_rating, service_factor)
    )

    periods = find_continuous_periods(df, 'condition')
    return periods

# Challenge 3: Calculate cost of energy wasted in vampire/idle states
def challenge_3():
    motor_rating = calculate_motor_rating()
    service_factor = 1.2

    df = pd.read_csv('energy.csv')
    df.columns = df.columns.str.strip()
    df['total_power_kw'] = (df['p1'] + df['p2'] + df['p3']) / 1000
    df['condition'] = df['total_power_kw'].apply(
        lambda x: classify_power(x, motor_rating, service_factor)
    )

    costs = {}
    for condition in ['vampire', 'idle']:
        condition_df = df[df['condition'] == condition]
        total_cost = 0

        for _, row in condition_df.iterrows():
            rate = get_tariff_rate(row['time'])
            energy_kwh = row['energy'] / 1000
            total_cost += energy_kwh * rate

        costs[condition] = int(total_cost)

    return costs

if __name__ == "__main__":
    try:
        c1 = challenge_1()
        c2 = challenge_2()
        c3 = challenge_3()

        print("\nChallenge 1 - Energy Consumption (kWh):")
        print(c1)

        print("\nChallenge 2 - Duration Periods:")
        print(c2)

        print("\nChallenge 3 - Energy Costs (paise):")
        print(c3)

    except FileNotFoundError:
        print("\nError: Could not find 'power.csv' or 'energy.csv'.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")