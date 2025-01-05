import csv
from datetime import datetime, timedelta
import random
import pytz

# Configurations
time_zone = pytz.timezone('Asia/Ho_Chi_Minh')
end_date = datetime.now(time_zone)
start_date = end_date - timedelta(days=4)
time_interval = timedelta(minutes=5)
api_key = '1'

# Sensor configurations with their respective value ranges
sensors = [
    {'pin': 'V8', 'name': 'Độ Ẩm Không Khí', 'base_range': (22.0, 24.0)},
    {'pin': 'V7', 'name': 'Nhiệt Độ Không Khí', 'base_range': (55.0, 65.0)},
    {'pin': 'V5', 'name': 'Nhiệt Độ Nước', 'base_range': (19.0, 22.0)},
    {'pin': 'V9', 'name': 'Cảm biến PH', 'base_range': (5.5, 6.5)},
    {'pin': 'V6', 'name': 'Ánh sáng', 'base_range': (0.0, 100.0)}
]

# Helper function to adjust range based on time
def adjust_range(sensor, current_time):
    """
    Adjust the range of sensor values based on the current time of day.
    """
    hour = current_time.hour

    if sensor['name'] == 'Nhiệt Độ Không Khí':
        # Nhiệt độ không khí thay đổi vào ban ngày (tăng thêm 5 độ)
        if 6 <= hour < 18:  # Daytime
            return (sensor['base_range'][0] + 5, sensor['base_range'][1] + 5)
    elif sensor['name'] == 'Độ Ẩm Không Khí':
        # Độ ẩm không khí tăng vào ban đêm
        if hour < 6 or hour >= 18:  # Nighttime
            return (sensor['base_range'][0] + 10, sensor['base_range'][1] + 10)
    elif sensor['name'] == 'Ánh sáng':
        # Ánh sáng thay đổi mạnh giữa ban ngày và ban đêm
        if 6 <= hour < 18:  # Daytime
            return (70.0, 90.0)
        else:  # Nighttime
            return (0.0, 10.0)
    # Các cảm biến khác không thay đổi theo thời gian
    return sensor['base_range']

# Generate data
data = []
current_time = end_date
while current_time >= start_date:
    for sensor in sensors:
        adjusted_range = adjust_range(sensor, current_time)
        value = round(random.uniform(*adjusted_range), 1)
        data.append([
            api_key, 
            sensor['pin'], 
            sensor['name'], 
            value, 
            current_time.strftime('%Y-%m-%d %H:%M:%S')
        ])
    current_time -= time_interval

# Write to CSV
output_file = 'sensors_data.csv'
with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['api_key', 'pin', 'name', 'value', 'date'])
    csvwriter.writerows(data)

print(f"Generated {len(data)} rows of data. File saved as '{output_file}'.")
