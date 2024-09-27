import sys, os
import logging
from flask import Flask, render_template, request
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from dbhelper import DB

application = Flask(__name__)
db = DB()

# Configure logging
log_dir = '/var/log/3USFlights'
os.makedirs(log_dir, exist_ok=True)

log_file_path = os.path.join(log_dir, 'app.log')
file_handler = logging.FileHandler(log_file_path)
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

application.logger.addHandler(file_handler)
application.logger.setLevel(logging.DEBUG)

# Also print to stdout for immediate feedback (optional)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)
application.logger.addHandler(console_handler)

@application.route('/')
def index():
    return render_template('index.html')

@application.route('/check_flights', methods=['get', 'post'])
def check_flights():
    dep_city = None
    arr_city = None
    if request.method == 'POST':
        application.logger.info('Received POST request for check_flights')
        dep_city = request.form.get('dep_city')
        arr_city = request.form.get('arr_city')
        if dep_city and arr_city:
            application.logger.info(f'Fetching flights from {dep_city} to {arr_city}')
            try:
                results = db.fetch_all_flights(dep_city, arr_city)
                return render_template('check_flights.html', results=results, dep_city=dep_city, arr_city=arr_city)
            except Exception as e:
                application.logger.error(f"Error fetching flights: {e}")

    application.logger.info('Handling GET request for check_flights')
    city_names = sorted(db.fetch_city_names())
    return render_template('check_flights.html', city_names=city_names, dep_city=dep_city, arr_city=arr_city)

@application.route('/analytics')
def analytics():
    try:
        airline, frequency = db.fetch_airline_frequency()
        pie_fig = go.Figure(go.Pie(labels=airline, values=frequency, hoverinfo="label+percent", textinfo="value"))
        pie_chart = pie_fig.to_html(full_html=False)
    except Exception as e:
        application.logger.error(f"Error generating pie chart: {e}")
        pie_chart = "Error generating chart"

    try:
        city, frequency1 = db.busy_airport()
        bar_fig = px.bar(x=city, y=frequency1, labels={'x': 'City', 'y': 'Frequency'}, title='Busy Airports')
        bar_chart = bar_fig.to_html(full_html=False)
    except Exception as e:
        application.logger.error(f"Error generating bar chart: {e}")
        bar_chart = "Error generating chart"

    try:
        date, frequency2 = db.daily_frequency()
        line_fig = px.line(x=date, y=frequency2, labels={'x': 'Date', 'y': 'Frequency'}, title='Daily Flight Frequency')
        line_chart = line_fig.to_html(full_html=False)
    except Exception as e:
        application.logger.error(f"Error generating line chart: {e}")
        line_chart = "Error generating chart"

    return render_template('analytics.html', pie_chart=pie_chart, bar_chart=bar_chart, line_chart=line_chart)

if __name__ == '__main__':
    application.run(debug=True)
