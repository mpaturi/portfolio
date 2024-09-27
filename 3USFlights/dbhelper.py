import os
import time
import logging
import pyodbc
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager

class DB:
    def __init__(self):
        # Ensure the log directory exists
        self.log_dir = '/var/log/3USFlights'
        os.makedirs(self.log_dir, exist_ok=True)

        # Set up logging
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        log_file_path = os.path.join(self.log_dir, 'app.log')
        handler = logging.FileHandler(log_file_path)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        # Console handler for immediate feedback
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        self.logger.debug("Logger initialized and ready to use.")
        self.logger.info("Starting the database connection setup.")

        try:
            # Retrieve the DSN for AWS MySQL from environment variable
            self.dsn = os.getenv('DB_DSN', 'AWSMYSQL')

            # Create the connection string using the DSN for SQLAlchemy
            self.connection_string = f"mysql+pyodbc:///?dsn={self.dsn}&pool_size=20&max_overflow=0&pool_timeout=60&pool_recycle=3600"

            # Create the SQLAlchemy engine with connection pooling
            self.engine = create_engine(self.connection_string)

            # Direct pyodbc connection setup
            self.pyodbc_connection_string = f"DSN={self.dsn}"
            self.pyodbc_conn = None
            self.connect()

            self.logger.info("Connection setup successful!")
        except SQLAlchemyError as e:
            self.logger.error(f"Database connection error: {e}")
            raise
        except Exception as e:
            # Log any other exceptions that may occur
            self.logger.error(f"Unexpected error: {e}")
            raise

    @contextmanager
    def get_connection(self):
        """Context manager to handle SQLAlchemy database connections."""
        connection = None
        try:
            connection = self.engine.connect()
            yield connection
        except SQLAlchemyError as e:
            self.logger.error(f"Connection error: {e}")
            raise
        finally:
            if connection:
                connection.close()

    def connect(self):
        """Try to establish a direct connection using pyodbc."""
        max_retries = 5
        for attempt in range(max_retries):
            try:
                self.pyodbc_conn = pyodbc.connect(self.pyodbc_connection_string)
                self.logger.info("Successfully connected to the database using pyodbc.")
                break
            except Exception as e:
                self.logger.error(f"Connection attempt {attempt + 1} failed: {e}")
                time.sleep(5)  # Wait before retrying
        else:
            self.logger.critical("Unable to connect to the database using pyodbc after several attempts.")
            raise Exception("Database connection failed")

    def fetch_city_names(self):
        city = []
        try:
            query = text("""
                SELECT DISTINCT Dep_CityName FROM flights.usflightsjan1wk
                UNION
                SELECT DISTINCT Arr_CityName FROM flights.usflightsjan1wk
            """)
            self.logger.debug(f'Executing query to fetch city names: {query}')
            with self.get_connection() as connection:
                result = connection.execute(query)
                data = result.fetchall()
                city = [item[0] for item in data]
            self.logger.info('City names fetched successfully.')
        except Exception as e:
            self.logger.error(f"Error fetching city names: {e}")
        return city

    def fetch_all_flights(self, source, destination):
        data = []
        try:
            query = text("""
                SELECT Airline, DepTime_label, Flight_Duration, Distance_type 
                FROM flights.usflightsjan1wk
                WHERE Dep_CityName = :source AND Arr_CityName = :destination
            """)
            self.logger.debug(f'Executing query to fetch flights: {query} with source={source} and destination={destination}')
            with self.get_connection() as connection:
                result = connection.execute(query, {'source': source, 'destination': destination})
                data = result.fetchall()
            self.logger.info('All flights fetched successfully.')
        except Exception as e:
            self.logger.error(f"Error fetching all flights: {e}")
        return data

    def fetch_airline_frequency(self):
        airline = []
        frequency = []
        try:
            query = text("""
                SELECT Airline, COUNT(*) 
                FROM flights.usflightsjan1wk
                GROUP BY Airline
            """)
            self.logger.debug(f'Executing query to fetch airline frequency: {query}')
            with self.get_connection() as connection:
                result = connection.execute(query)
                data = result.fetchall()
                airline = [item[0] for item in data]
                frequency = [item[1] for item in data]
            self.logger.info('Airline frequency data fetched successfully.')
        except Exception as e:
            self.logger.error(f"Error fetching airline frequency: {e}")
        return airline, frequency

    def busy_airport(self):
        city = []
        frequency = []
        try:
            query = text("""
                SELECT Dep_CityName, COUNT(*) 
                FROM (SELECT Dep_CityName FROM flights.usflightsjan1wk
                UNION ALL
                SELECT Arr_CityName FROM flights.usflightsjan1wk) t
                GROUP BY t.Dep_CityName
                ORDER BY COUNT(*) DESC
            """)
            self.logger.debug(f'Executing query to fetch busy airports: {query}')
            with self.get_connection() as connection:
                result = connection.execute(query)
                data = result.fetchall()
                city = [item[0] for item in data]
                frequency = [item[1] for item in data]
            self.logger.info('Busy airport data fetched successfully.')
        except Exception as e:
            self.logger.error(f"Error fetching busy airports: {e}")
        return city, frequency

    def daily_frequency(self):
        date = []
        frequency = []
        try:
            query = text("""
                SELECT FlightDate, COUNT(*) 
                FROM flights.usflightsjan1wk
                GROUP BY FlightDate
            """)
            self.logger.debug(f'Executing query to fetch daily frequency: {query}')
            with self.get_connection() as connection:
                result = connection.execute(query)
                data = result.fetchall()
                date = [item[0] for item in data]
                frequency = [item[1] for item in data]
            self.logger.info('Daily frequency data fetched successfully.')
        except Exception as e:
            self.logger.error(f"Error fetching daily frequency: {e}")
        return date, frequency

    def close(self):
        # Properly close the SQLAlchemy engine
        if self.engine:
            self.engine.dispose()
            self.logger.info("Database connection closed.")

        # Properly close the pyodbc connection
        if self.pyodbc_conn:
            self.pyodbc_conn.close()
            self.logger.info("Direct database connection closed.")

    def __del__(self):
        try:
            self.close()
        except Exception as e:
            self.logger.error(f"Exception in __del__: {e}")
