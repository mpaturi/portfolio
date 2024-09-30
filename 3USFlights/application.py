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
file_handler.setLevel(logging.WARNING)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

application.logger.addHandler(file_handler)
application.logger.setLevel(logging.WARNING)

# Also print to stdout for immediate feedback (optional)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.WARNING)
console_handler.setFormatter(formatter)
application.logger.addHandler(console_handler)

@application.route('/')
def index():
    return render_template('index.html')

@application.route('/check_flights', methods=['GET', 'POST'])
def check_flights():
    dep_city = request.form.get('dep_city', '')
    arr_city = request.form.get('arr_city', '')
    arr_delay = request.form.get('arr_delay', '')

    if request.method == 'POST':
        if dep_city and arr_city and arr_delay:
            application.logger.info(f'Fetching flights from {dep_city} to {arr_city} with '
                                    f'arrival delay more than{arr_delay}')
            try:
                results = db.fetch_all_flights(dep_city, arr_city, arr_delay)
                # Check if results are empty
                if not results:
                    no_flights_message = "There are no flights between these cities, please select another city or cities."
                    return render_template('check_flights.html',
                                           results=results,
                                           city_names=sorted(db.fetch_city_names()),
                                           dep_city=dep_city,
                                           arr_city=arr_city,
                                           arr_delay=arr_delay,
                                           no_flights_message=no_flights_message)

                return render_template('check_flights.html',
                                       results=results,
                                       city_names=sorted(db.fetch_city_names()),
                                       dep_city=dep_city,
                                       arr_city=arr_city,
                                       arr_delay=arr_delay)
            except Exception as e:
                application.logger.error(f"Error fetching flights: {e}")
                return render_template('check_flights.html',
                                       error="Could not fetch flights. Please try again.",
                                       city_names=sorted(db.fetch_city_names()),
                                       dep_city=dep_city,
                                       arr_city=arr_city,
                                       arr_delay=arr_delay)

    application.logger.info('Handling GET request for check_flights')
    city_names = sorted(db.fetch_city_names())
    return render_template('check_flights.html',
                           city_names=city_names,
                           dep_city=dep_city,
                           arr_city=arr_city,
                           arr_delay=arr_delay)

@application.route('/analytics')
def analytics():
    try:
        airline, frequency = db.fetch_airline_frequency()
        pie_fig = go.Figure(go.Pie(labels=airline, values=frequency, hoverinfo="label+percent", textinfo="value"))
        pie_chart = pie_fig.to_html(full_html=False)
    except Exception as e:
        application.logger.error(f"Error generating pie chart: {e}")

    try:
        city, frequency1 = db.busy_airport()
        bar_fig = px.bar(x=city, y=frequency1, labels={'x': 'City', 'y': 'Frequency'})
        bar_chart = bar_fig.to_html(full_html=False)
    except Exception as e:
        application.logger.error(f"Error generating bar chart: {e}")

    try:
        date, frequency2 = db.daily_frequency()
        line_fig = px.line(x=date, y=frequency2, labels={'x': 'Date', 'y': 'Frequency'})
        line_chart = line_fig.to_html(full_html=False)
    except Exception as e:
        application.logger.error(f"Error generating line chart: {e}")

    return render_template('analytics.html', pie_chart=pie_chart, bar_chart=bar_chart, line_chart=line_chart)

if __name__ == '__main__':
    application.run(debug=True)
