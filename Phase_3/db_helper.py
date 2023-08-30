"""
The module to make single instance of db connection within the program.
"""
import mysql.connector


class DbConnector:
    def __init__(self, host="localhost", user="root", password="CS6400DB"):
        """
        Initializing a DbConnector instance that connects to the database
        """
        self.host = host
        self.user = user
        self.password = password
        self._init_conn()
    
    def _init_conn(self):
        self.conn = mysql.connector.connect(host=self.host,user=self.user, password=self.password)

    def get_conn(self):
        return self.conn

    def close_conn(self):
        self.conn.close()

# create the only instance
dbConn = DbConnector()

def execute_sql_script(conn, filename):
    cursor = conn.cursor()
    with open(filename, 'r') as fd:
        sqlFile = fd.read()
    sqlCommands = sqlFile.split(';')
    for command in sqlCommands:
        command = command.strip()
        if command:
            cursor.execute(command)
    conn.commit()
    cursor.close()

def create_tables():
    execute_sql_script(dbConn.get_conn(), 'schema/CreateTables.sql')

def create_testdata():
    execute_sql_script(dbConn.get_conn(), 'test/demo_location.sql')
    execute_sql_script(dbConn.get_conn(), 'test/demo_household.sql')
    execute_sql_script(dbConn.get_conn(), 'test/demo_manufacturer.sql')
    execute_sql_script(dbConn.get_conn(), 'test/demo_public_ultility.sql')
    execute_sql_script(dbConn.get_conn(), 'test/demo_appliance.sql')
    execute_sql_script(dbConn.get_conn(), 'test/demo_waterheater.sql')
    execute_sql_script(dbConn.get_conn(), 'test/demo_power_generator.sql')
    execute_sql_script(dbConn.get_conn(), 'test/demo_air_handler.sql')
    execute_sql_script(dbConn.get_conn(), 'test/demo_air_conditioner.sql')
    execute_sql_script(dbConn.get_conn(), 'test/demo_heater.sql')
    execute_sql_script(dbConn.get_conn(), 'test/demo_heat_pump.sql')

def drop_tables():
    execute_sql_script(dbConn.get_conn(), 'schema/DropTables.sql')


if __name__ == '__main__':
    create_tables()
    #drop_tables()
    #create_testdata()
