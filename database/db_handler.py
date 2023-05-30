import logging

import psycopg2
from psycopg2 import OperationalError
from dotenv import dotenv_values

from database.db_config import DB_CONNECTION_ARGS

config = dotenv_values("../.env")


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


def execute_query(connection, query, insert_data=None):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        if insert_data:
            cursor.execute(query, insert_data)
        else:
            cursor.execute(query)
            query_result = cursor.fetchall()
            if query_result:
                return query_result
        print("Query executed successfully")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    finally:
        cursor.close()
        connection.close()


def insert_data_into_volunteers_table(data: list):
    if not data:
        raise ValueError("Data list should not be empty.")
    connection = create_connection(*DB_CONNECTION_ARGS)
    data_records = ", ".join(["%s"] * len(data))
    insert_query = (
        f"INSERT INTO volunteers (first_name, last_name, phone_number) VALUES {data_records}"
    )
    execute_query(connection, insert_query, data)
    success_info = f"Data inserted into volunteers table in DB db_volunteers."
    logging.info(success_info)
    print(success_info)


def get_all_volunteers(connection):
    all_volunteers = execute_query(connection, "SELECT * FROM volunteers")
    return all_volunteers


def get_volunteer_by(param_name, param_value, connection):
    query = f"SELECT * FROM volunteers WHERE {param_name}={param_value}"
    volunteers_by_param = execute_query(connection, query)
    return volunteers_by_param


def get_volunteer_by_id(id: int, connection):
    if not id:
        raise ValueError("ID should not be empty.")
    return get_volunteer_by("volunteer_id", id, connection)


# print(get_all_volunteers(create_connection(*DB_CONNECTION_ARGS)))
# dodac funkcje get_all_staff_members() i pozniej w controllerze endpoint na to.
# Funkcja niech wyrzuca bledy np. raise valueError kiedy tabela jest pusta lub nie istnieje lub gdy nie udalo sie polaczenie z baza danych.
# Chociaz polaczenie z baza danych juz jest sprawdzane w create connection try/except.
# Controller powinien przechwycic te bledy i przekazac klientowi numer bledu np. 405 wraz z trescia np. pusta baza danych etc.
# Dzieki temu jesli w db_handler cos sie skopie to po prostu wypycha blad do controllera a controller ten blad odpowiednio obrobi i wyrzuci do klienta.
