import requests
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import pytz
import os 

# Define the URL for the JSON data
url = "https://services.swpc.noaa.gov/products/noaa-planetary-k-index-forecast.json"

# Define a function to map Kp values to colors
def map_kp_to_color(kp):
    if kp < 5:
        return 'green'
    elif 5 <= kp < 6:
        return 'yellow'
    elif 6 <= kp < 7:
        return 'gold'
    elif 7 <= kp < 8:
        return 'orange'
    elif 8 <= kp < 9:
        return 'red'
    else:
        return 'darkred'

try:
    # Send a GET request to fetch the JSON data
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        # Extract data for plotting
        timestamps = []
        kp_values = []
        colors = []

        # Initialize variables to track the highest probability of Aurora
        highest_kp = 0
        highest_kp_time = None

        # Initialize the previous date
        prev_date = None

        # Define time zones for UTC and EST
        utc_timezone = pytz.timezone('UTC')
        est_timezone = pytz.timezone('US/Eastern')

        # Skip the header row (data[0]) and process the rest of the data
        for entry in data[1:]:
            time_str = entry[0]
            kp = float(entry[1])
            current_date_utc = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
            current_date_est = current_date_utc.astimezone(est_timezone)

            if current_date_est.date() != prev_date:
                timestamps.append(current_date_est)
                kp_values.append(kp)
                colors.append(map_kp_to_color(kp))
                prev_date = current_date_est.date()
            else:
                timestamps.append(current_date_est)
                kp_values.append(kp)
                colors.append(map_kp_to_color(kp))

            # Check if the current Kp value is higher than the previous highest
            if kp > highest_kp:
                highest_kp = kp
                highest_kp_time = current_date_est

        # Create the bar graph with removed lines and double-width columns
        plt.figure(figsize=(12, 6))
        plt.bar(timestamps, kp_values, color=colors, width=0.04)  # Adjust width as needed (doubled)
        plt.title('Planetary K-index (Kp) Forecast')
        plt.xlabel('Date and Time (EST)')
        plt.ylabel('Kp Value')
        plt.grid(axis='y', linestyle='--', alpha=0.7)  # Remove vertical grid lines
        plt.ylim(0, 9)
        plt.xticks(rotation=45)

        # Set x-axis labels to display the date only on the first data point of a day
        date_labels = [timestamp.strftime('%Y-%m-%d') if timestamp.hour == 0 else "" for timestamp in timestamps]
        plt.xticks(timestamps, date_labels)

        # Save the graph as a PNG image
        script_directory = "/home/pi/RFIDPiServer/static"
        image_path = os.path.join(script_directory, 'solar_weather_graph.png')
        print("printing picture")
        plt.tight_layout()
        plt.savefig(image_path, format='png', dpi=300)


        # Display the highest probability of Aurora below the graph
        if highest_kp_time:
            highest_kp_text = f"The highest probability of Aurora will occur on {highest_kp_time.strftime('%Y-%m-%d')} at {highest_kp_time.strftime('%H:%M')} EST"
            plt.text(0.5, -0.15, highest_kp_text, fontsize=12, ha="center", transform=plt.gca().transAxes)

        plt.show()

    else:
        print(f"HTTP error: {response.status_code}")

except requests.exceptions.RequestException as req_err:
    print(f"Request error: {req_err}")
