from flask import Flask, render_template, request, jsonify
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from dbhelper import DB

application = Flask(__name__)
db = DB()

@application.route('/')
def index():
    return render_template('index.html')

@application.route('/check_flights', methods=['get', 'post'])
def check_flights():
    dep_city = None
    arr_city = None
    #dep_city = request.form.get('dep_city')
    #arr_city = request.form.get('arr_city')
    if request.method == 'POST':
        print('in check_flights post')
        dep_city = request.form.get('dep_city')
        arr_city = request.form.get('arr_city')
        if dep_city and arr_city:
            print('in check_flights fetch')
            results = db.fetch_all_flights(dep_city, arr_city)
            print(results)
            return render_template('check_flights.html', results=results, dep_city=dep_city, arr_city=arr_city)
            # try:
            #     results = db.fetch_all_flights(dep_city, arr_city)
            # except Exception as e:
            #     app.logger.error(f"Error fetching flights: {e}")

    print('in check_flights get')
    city_names = sorted(db.fetch_city_names())
    print(city_names)
    return render_template('check_flights.html', city_names=city_names,dep_city=dep_city, arr_city=arr_city)

@application.route('/analytics')
def analytics():
    # Airline frequency pie chart
    try:
        airline, frequency = db.fetch_airline_frequency()
        pie_fig = go.Figure(
            go.Pie(
                labels=airline,
                values=frequency,
                hoverinfo="label+percent",
                textinfo="value"
            )
        )
        pie_chart = pie_fig.to_html(full_html=False)
    except Exception as e:
        application.logger.error(f"Error generating pie chart: {e}")
        pie_chart = "Error generating chart"

    # Busy airports bar chart
    try:
        city, frequency1 = db.busy_airport()
        bar_fig = px.bar(
            x=city,
            y=frequency1,
            labels={'x': 'City', 'y': 'Frequency'},
            title='Busy Airports'
        )
        bar_chart = bar_fig.to_html(full_html=False)
    except Exception as e:
        application.logger.error(f"Error generating bar chart: {e}")
        bar_chart = "Error generating chart"

    # Daily frequency line chart
    try:
        date, frequency2 = db.daily_frequency()
        line_fig = px.line(
            x=date,
            y=frequency2,
            labels={'x': 'Date', 'y': 'Frequency'},
            title='Daily Flight Frequency'
        )
        line_chart = line_fig.to_html(full_html=False)
    except Exception as e:
        application.logger.error(f"Error generating line chart: {e}")
        line_chart = "Error generating chart"

    return render_template('analytics.html', pie_chart=pie_chart, bar_chart=bar_chart, line_chart=line_chart)


if __name__ == '__main__':
    # Use the default Flask port and host
    #application.run(debug=True, host='0.0.0.0')
    application.run(debug=True)