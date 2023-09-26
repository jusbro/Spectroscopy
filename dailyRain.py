import requests
import matplotlib.pyplot as plt
import json
from matplotlib.ticker import MaxNLocator

# Define the API URL
api_url = "https://api.open-meteo.com/v1/forecast?latitude=40.5556&longitude=-75.9819&hourly=precipitation_probability&temperature_unit=fahrenheit&windspeed_unit=mph&precipitation_unit=inch&timezone=America%2FNew_York"

try:
    # Send a GET request to fetch the data
    response = requests.get(api_url)

    if response.status_code == 200:
        # Parse the JSON response
        data = json.loads(response.text)

        # Extract relevant data
        timestamps = data["hourly"]["time"]
        precipitation_probability = data["hourly"]["precipitation_probability"]

        # Create the graph
        plt.figure(figsize=(12, 6))
        plt.plot(timestamps, precipitation_probability, marker='o', linestyle='-', color='b')
        plt.title('Hourly Precipitation Forecast for Hamburg, PA.')
        plt.xlabel('Time')
        plt.ylabel('% Chance Precipitation')
        plt.grid(True)

        # Set custom x-axis tick locator and formatter
        ax = plt.gca()
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))  # Display integers on the x-axis
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: timestamps[int(x)][:16] if int(x) < len(timestamps) else ""))

        plt.xticks(rotation=10)

        plt.tight_layout()

        # Save the graph as an image
        plt.savefig("percent_chance_precip_graph.png")

        # Display the graph
        plt.show()

    else:
        print(f"HTTP error: {response.status_code}")

except requests.exceptions.RequestException as req_err:
    print(f"Request error: {req_err}")
except KeyError as key_err:
    print(f"Key error: {key_err}")
