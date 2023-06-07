import logging

import psycopg2
from psycopg2 import OperationalError
from dotenv import dotenv_values
from sqlalchemy import exc

from database.db_config import DB_CONNECTION_ARGS
from models import Volunteer
from exceptions import NoRecordFound

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
        f"INSERT INTO volunteers (first_name, last_name, phone_number) VALUES ({data_records})"
    )
    execute_query(connection, insert_query, data)
    success_info = f"Data inserted into volunteers table in DB db_volunteers."
    logging.info(success_info)
    print(success_info)


def db_add_volunteer(volunteer, db_model):
    db_model.session.add(volunteer)
    db_model.session.commit()
    return print(f'Volunteer {volunteer.first_name} {volunteer.last_name} added to DB')


def db_delete_volunteer(volunteer, db_model):
    db_model.session.delete(volunteer)
    db_model.session.commit()
    return print(f'Volunteer {volunteer.first_name} {volunteer.last_name} deleted from DB')


def get_all_volunteers(connection):
    all_volunteers = execute_query(connection, "SELECT * FROM volunteers")
    return all_volunteers


def get_volunteer_by(param_name, param_value, connection):
    query = f"SELECT * FROM volunteers WHERE {param_name}={param_value}"
    volunteers_by_param = execute_query(connection, query)
    return volunteers_by_param


# def get_volunteer_by_id(volunteer_id: int, connection):
#     if not volunteer_id:
#         raise ValueError("ID should not be empty.")
#     volunteer_by_id = get_volunteer_by("volunteer_id", volunteer_id, connection)
#     if not volunteer_by_id:
#         return ValueError(f"Volunteer with ID={volunteer_id} doesn't exist.")
#     return volunteer_by_id

def get_volunteer_by_id(volunteer_id: int):
    try:
        volunteer = Volunteer.query.filter_by(volunteer_id=volunteer_id).one()
    except exc.NoResultFound as e:
        #     TO_DO: Logger with original error message logger.warning(e.message)
        raise NoRecordFound
    return volunteer


# dodac funkcje get_all_staff_members() i pozniej w controllerze endpoint na to.
# Funkcja niech wyrzuca bledy np. raise valueError kiedy tabela jest pusta lub nie istnieje lub gdy nie udalo sie polaczenie z baza danych.
# Chociaz polaczenie z baza danych juz jest sprawdzane w create connection try/except.
# Controller powinien przechwycic te bledy i przekazac klientowi numer bledu np. 405 wraz z trescia np. pusta baza danych etc.
# Dzieki temu jesli w db_handler cos sie skopie to po prostu wypycha blad do controllera a controller ten blad odpowiednio obrobi i wyrzuci do klienta.
