from flask import Flask, render_template
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/solar_weather')
def solar_weather():
    try:
        # Run the solarSpaceWeather.py script as a separate process
        subprocess.run(['python', 'solar_space_weather.py'])
    except Exception as e:
        return f"Error: {str(e)}"

    # Pass the image URL to the template
    image_url = "/static/solar_weather_graph.png"

    # Render the HTML template with the image URL
    return render_template('solar_weather.html', image_url=image_url)

@app.route('/local_weather')
def local_weather():
    try:
        # Run the solarSpaceWeather.py script as a separate process
        subprocess.run(['python', 'dailyTemp.py'])
    except Exception as e:
        return f"Error: {str(e)}"

    # Pass the image URL to the template
    image_url = "/static/temperature_graph.png"

    # Render the HTML template with the image URL
    return render_template('local_weather.html', image_url=image_url)
    try:
        # Run the solarSpaceWeather.py script as a separate process
        subprocess.run(['python', 'dailyRain.py'])
    except Exception as e:
        return f"Error: {str(e)}"

    # Pass the image URL to the template
    image_url = "/static/temperature_graph.png"

    # Render the HTML template with the image URL
    return render_template('local_weather.html', image_url=image_url)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
