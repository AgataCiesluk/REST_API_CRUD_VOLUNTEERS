import psycopg2
from psycopg2 import OperationalError
from dotenv import dotenv_values

config = dotenv_values(".env")
conn_args = [
    config.get("DB_NAME"),
    config.get("DB_USER"),
    config.get("DB_PASSWORD"),
    config.get("DB_HOST"),
    config.get("DB_PORT")]

def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection


def execute_get_query(connection, query):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Query executed successfully")
    except OperationalError as e:
        print(f"The error '{e}' occurred")


# Create DB if not exist
# conn_postgres = create_connection(
#     "postgres",
#     config.get("DB_USER"),
#     config.get("DB_PASSWORD"),
#     config.get("DB_HOST"),
#     config.get("DB_PORT")
# )
# create_database_query = "CREATE DATABASE volunteers"
# execute_get_query(conn_postgres, create_database_query)
conn_volunteers = create_connection(*conn_args)
