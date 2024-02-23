import sqlite3
import requests
from modules.stationInformation import stationInforamtion
from modules.vehicle import vehicle
from modules.stationStatus import stationStatus
from modules.freeBike import freeBike

class apiCalling:

    def __init__(self):
        self.baseURL = 'https://gbfs.nextbike.net/maps/gbfs/v2/'
        self.conn = None

    def callingAPI(self, endPoints):
        url = self.baseURL + endPoints
        response = requests.get(url)

        if response.status_code == 200:
            responseData = response.json()
            return responseData['data'][next(iter(responseData['data']))]
        else:
            raise Exception(f"API request failed with status code {response.status_code}")

    def ConnectionToDatabase(self):
        self.conn = sqlite3.connect('nextbike.db')

    def createTableIfNotExists(self):
        try:
            if self.conn is not None:
                cursor = self.conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS stations (
                        station_id INTEGER PRIMARY KEY,
                        name TEXT,
                        short_name TEXT,
                        lat REAL,
                        lon REAL,
                        region_id TEXT,
                        is_virtual_station INTEGER,
                        capacity INTEGER
                    )
                """)

                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS vehicles (
                        vehicle_type_id INTEGER PRIMARY KEY,
                        vehicle_image TEXT NOT NULL,
                        name TEXT,
                        rider_capacity INTEGER,
                        propulsion_type TEXT,
                        max_range_meters INTEGER
                    )
                """)
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS station_status (
                        station_id INTEGER REFERENCES stations(station_id),
                        num_bikes_available INTEGER,
                        num_docks_available INTEGER,
                        is_installed TEXT,
                        is_renting INTEGER,
                        is_returning INTEGER,
                        last_reportes TEXT
                    )
                """)
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS free_bike (
                        bike_id TEXT PRIMARY KEY,
                        is_reserved INTEGER,
                        is_disabled INTEGER,
                        lat REAL,
                        lon REAL,
                        vehicle_type_id INTEGER REFERENCES vehicles(vehicle_type_id),
                        station_id INTEGER REFERENCES stations(station_id),
                        pricing_plan_id TEXT
                    )
                """)

                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS user_details(
                        user_id TEXT PRIMARY KEY,
                        user_name TEXT,
                        email_address TEXT,
                        phone_number INTEGER,
                        gender TEXT,
                        password TEXT,
                        role_type TEXT
                    )
                """)

                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS user_card_details(
                        user_id  TEXT REFERENCES user_details(user_id),
                        card_number INTEGER,
                        card_name TEXT,
                        card_cvv TEXT
                    )
                """)

                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS security_questions(
                        question_index TEXT PRIMARY KEY,
                        question_text TEXT
                    )
                """)

                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS user_security_question(
                        user_id TEXT PRIMARY KEY,
                        question_index TEXT REFERENCES security_questions(question_index),
                        question_answer TEXT
                    )
                """)

                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS bike_in_use(
                        ID TEXT PRIMARY KEY,
                        user_id TEXT,
                        bike_id TEXT,
                        station_from TEXT,
                        station_to TEXT,
                        start_time TIMESTAMP,
                        end_time TIMESTAMP,
                        duration REAL
                    )
                """)
                

                self.conn.commit()
        except Exception as e:
            print("There is some error in creating the table", str(e))

    def insertDataIntostation(self):
        dataFromAPI = self.callingAPI('nextbike_gg/en/station_information.json')
        cursor = self.conn.cursor()
        insert_sql = """
            INSERT INTO stations (station_id, name, short_name, lat, lon, region_id, is_virtual_station, capacity)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        for data in dataFromAPI:
            if 'capacity' in data:
                record = (data['station_id'], data['name'], data['short_name'], data['lat'], data['lon'], data['region_id'], data['is_virtual_station'], data['capacity'])
            else:
                record = (data['station_id'], data['name'], data['short_name'], data['lat'], data['lon'], data['region_id'], data['is_virtual_station'], 0)
            cursor.execute(insert_sql, record)
        self.conn.commit()

    def insertDataIntoVehicleType(self):
        dataFromAPI = self.callingAPI('nextbike_gg/en/vehicle_types.json')
        cursor = self.conn.cursor()
        insert_sql = """
            INSERT INTO vehicles (vehicle_type_id, vehicle_image, name, rider_capacity, propulsion_type, max_range_meters)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        for data in dataFromAPI:
            if 'max_range_meters' in data:
                record = (data['vehicle_type_id'], data['vehicle_image'], data['name'], data['rider_capacity'], data['propulsion_type'], data['max_range_meters'])
            else:
                record = (data['vehicle_type_id'], data['vehicle_image'], data['name'], data['rider_capacity'], data['propulsion_type'], 0)
            cursor.execute(insert_sql, record)

    def insertDataIntoStationStatus(self):
        dataFromAPI = self.callingAPI('nextbike_gg/en/station_status.json')
        cursor = self.conn.cursor()
        insert_sql = """
            INSERT INTO station_status (station_id, num_bikes_available, num_docks_available, is_installed, is_renting, is_returning)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        for data in dataFromAPI:
            record = (data['station_id'], data['num_bikes_available'], data['num_docks_available'], data['is_installed'], data['is_renting'], data['is_returning'])
            cursor.execute(insert_sql, record)
        self.conn.commit()

    def insertDataIntoFreeBikeStatus(self):
        dataFromAPI = self.callingAPI('nextbike_gg/en/free_bike_status.json')
        cursor = self.conn.cursor()
        insert_sql = """
            INSERT INTO free_bike (bike_id, is_reserved, is_disabled, lat, lon, vehicle_type_id, station_id, pricing_plan_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        for data in dataFromAPI:
            if 'station_id' in data:
                record = (data['bike_id'], data['is_reserved'], data['is_disabled'], data['lat'], data['lon'], data['vehicle_type_id'], data['station_id'], data['pricing_plan_id'])
            else:
                record = (data['bike_id'], data['is_reserved'], data['is_disabled'], data['lat'], data['lon'], data['vehicle_type_id'], None, data['pricing_plan_id'])
            cursor.execute(insert_sql, record)
        self.conn.commit()

    def insertIntoSecurityQuestions(self):
        self.conn.execute("""INSERT INTO security_questions (question_text) VALUES
                    ('What is your mother''s maiden name?'),
                    ('What is the name of your first pet?'),
                    ('In what city were you born?'),
                    ('What is your favorite book?')
                """)
        self.conn.commit()

    
apiCall = apiCalling()
apiCall.ConnectionToDatabase()
apiCall.createTableIfNotExists()
apiCall.insertDataIntostation()
apiCall.insertDataIntoStationStatus()
apiCall.insertDataIntoVehicleType()
apiCall.insertDataIntoFreeBikeStatus()
apiCall.insertIntoSecurityQuestions()
