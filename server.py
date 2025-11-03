from flask import Flask, request, render_template
from weather import get_current_weather

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Weather App')

@app.route('/weather')
def get_weather():
    city = request.args.get('city', 'Pune City')
    country = request.args.get('country', 'IN')
    print(f"Fetching weather for: {city}, {country}")
    weather_data = get_current_weather(city, country)
    print(weather_data)
    return render_template(
        "weather.html",
        title=weather_data["name"],
        status=weather_data['weather'][0]["description"].capitalize(),
        temp=f"{weather_data['main']['temp']:.1f}",
        feels_like=f"{weather_data['main']['feels_like']:.1f}"
    )

if __name__ == '__main__':
    app.run(debug=True)
