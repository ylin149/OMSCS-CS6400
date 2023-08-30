import mysql.connector
import os

USE_DATABASE_SQL = "CS6400_Summer2023_Team025;"


def connect_db(host, user, password=''):
    # establishing the connection
    db = mysql.connector.connect(host="Localhost", user="root", password="CS6400DB")
    return db


def drop_and_create_database(db):
    #Creating a cursor object using the cursor() method
    cursor = db.cursor()

    # check database already exists.
    cursor.execute("DROP DATABASE IF EXISTS CS6400_Summer2023_Team025")

    # create a database
    cursor.execute('CREATE CS6400_Summer2023_Team025')


def execute_sql_script_file(cursor, filename):
    # Open and read the file as a single buffer
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()

    # all SQL commands (split on ';')
    sqlCommands = sqlFile.split(';')

    # Execute every command from the input file
    for command in sqlCommands:
        cursor.execute(command)


def check_and_remove_shared_data_json():
    if os.path.exists(SHARED_DATA_JSON):
        os.remove(SHARED_DATA_JSON)


def create_or_add_shared_data_json(data):
    with open(SHARED_DATA_JSON, 'w+') as file_object:
        if os.path.getsize(SHARED_DATA_JSON) > 0:
            stored_data = json.load(file_object)
            updated_data = stored_data.update(data)
            json.dump(updated_data, file_object)
        else:
            json.dump(data, file_object)


def retrieve_shared_data_json():
    with open(SHARED_DATA_JSON, 'r') as file_object:
        stored_data = json.load(file_object)
        return stored_data


# when passing in host, user, and password information to connect_db function
# you can remove the password parameter below if you don't need to pass in password
CONN = connect_db("localhost", "root", "")