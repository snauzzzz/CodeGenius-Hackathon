from flask import Flask, render_template
import requests
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

# Retrieve API key from environment variable
api_key = os.environ.get('API_KEY')

@app.route('/')
def index():
    # Fetch air quality data for different cities
    cities = ['New York', 'London', 'Tokyo', 'Beijing', 'Paris', 'Los Angeles', 'Berlin', 'Moscow', 'Seoul', 'Sydney']
    air_quality_data = {}

    for city in cities:
        response = requests.get(f'https://api.waqi.info/feed/{city}/?token={api_key}')
        data = response.json()
        aqi = data['data']['aqi']
        air_quality_data[city] = aqi

    # Create a bar chart of air quality for different cities
    plt.figure(figsize=(8, 6))
    plt.bar(air_quality_data.keys(), air_quality_data.values(), color='skyblue')
    plt.xlabel('City')
    plt.ylabel('AQI')
    plt.title('Air Quality Index (AQI) for Different Cities')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the plot as a PNG file
    plot_path = 'static/air_quality_plot.png'
    plt.savefig(plot_path)

    return render_template('index.html', plot_path=os.path.basename(plot_path))

if __name__ == '__main__':
    app.run(debug=True)
