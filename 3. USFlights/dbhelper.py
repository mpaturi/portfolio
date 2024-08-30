import pyodbc
import logging

class DB:

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.ERROR)  # Set log level if needed
        #connect to the AWS MSSQL database - portfolio.cpououw2sybk.us-east-2.rds.amazonaws.com
        try:
            server='oltp.cpououw2sybk.us-east-2.rds.amazonaws.com'
            username='admin'
            password='Admin1234'
            database='Flights'
            driver ='{ODBC Driver 17 for SQL Server}'
            connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'

            # Establish a connection
            self.connection = pyodbc.connect(connection_string)
            # Create a cursor from the connection
            self.mycursor = self.connection.cursor()
            print("Connection successful!")
        except Exception as e:
            self.logger.error(f"Database connection error: {e}")
            raise

    def fetch_city_names(self):
        city = []
        try:
            self.mycursor.execute("""
                    SELECT DISTINCT Dep_CityName FROM USFlightsJan1Wk
                    UNION
                    SELECT DISTINCT Arr_CityName FROM USFlightsJan1Wk
                    """)
            data = self.mycursor.fetchall()
            city = [item[0] for item in data]
        except Exception as e:
            self.logger.error(f"Error fetching city names: {e}")
        return city

    def fetch_all_flights(self, source, destination):
        data = []
        try:
            self.mycursor.execute("""
                    SELECT Airline, DepTime_label, Flight_Duration, Distance_type 
                    FROM USFlightsJan1Wk
                    WHERE Dep_CityName = ? AND Arr_CityName = ?
                    """, (source, destination))
            data = self.mycursor.fetchall()
        except Exception as e:
            self.logger.error(f"Error fetching all flights: {e}")
        return data

    def fetch_airline_frequency(self):
        airline = []
        frequency = []
        try:
            self.mycursor.execute("""
            SELECT Airline, COUNT(*) 
            FROM USFlightsJan1Wk
            GROUP BY Airline
            """)
            data = self.mycursor.fetchall()
            airline = [item[0] for item in data]
            frequency = [item[1] for item in data]
        except Exception as e:
            self.logger.error(f"Error fetching airline frequency: {e}")
        return airline, frequency

    def busy_airport(self):
        city = []
        frequency = []
        try:
            self.mycursor.execute("""
                    SELECT Dep_CityName, COUNT(*) 
                    FROM (SELECT Dep_CityName FROM USFlightsJan1Wk
                    UNION ALL
                    SELECT Arr_CityName FROM USFlightsJan1Wk) t
                    GROUP BY t.Dep_CityName
                    ORDER BY COUNT(*) DESC
                    """)
            data = self.mycursor.fetchall()
            city = [item[0] for item in data]
            frequency = [item[1] for item in data]
        except Exception as e:
            self.logger.error(f"Error fetching busy airports: {e}")
        return city, frequency

    def daily_frequency(self):
        date = []
        frequency = []
        try:
            self.mycursor.execute("""
                    SELECT FlightDate, COUNT(*) 
                    FROM USFlightsJan1Wk
                    GROUP BY FlightDate
                    """)
            data = self.mycursor.fetchall()
            date = [item[0] for item in data]
            frequency = [item[1] for item in data]
        except Exception as e:
            self.logger.error(f"Error fetching daily frequency: {e}")
        return date, frequency

    def __del__(self):
        # Ensure the connection is closed when the object is deleted
        if hasattr(self, 'connection'):
            self.connection.close()






