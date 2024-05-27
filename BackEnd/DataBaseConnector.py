import mysql.connector

class DataBaseConnector():
    def __init__(self) -> None:
        # Establishing a connection to the MySQL database
        self.connection = mysql.connector.connect(
            host="localhost",    # Hostname of the MySQL server
            user="moniaq",     # Username to connect to MySQL
            password="admin", # Password for the username
            database="moniaq" # Name of the database to connect to
        )
    def SaveRecord(self, data):
        # Create a new cursor
        cursor = self.connection.cursor()
        # SQL Insert query
        sql = "INSERT INTO records (id, co2, temperature, humidity, loc_lat, loc_long) VALUES (NULL, %s, %s, %s, %s, %s)"
        # Execute the query
        cursor.execute(sql, (data["co2"], data["temperature"], data["humidity"], data["loc_lat"], data["loc_long"]))
        # Commit the changes
        self.connection.commit()
        # Close the cursor
        cursor.close()