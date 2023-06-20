import logging

import psycopg2
from psycopg2 import OperationalError
from dotenv import dotenv_values
from sqlalchemy import exc

from database.db_config import DB_CONNECTION_ARGS
from models import Volunteer
from exceptions import NoRecordFound
from utils import models_list_to_dict

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


def db_add_volunteer(first_name, last_name, phone_number, db_model):
    volunteer = Volunteer(first_name, last_name, phone_number)
    db_model.session.add(volunteer)
    db_model.session.commit()
    return volunteer


def db_delete_volunteer(id, db_model):
    try:
        volunteer = get_volunteer_by_id(id)
    except NoRecordFound:
        raise
    db_model.session.delete(volunteer)
    db_model.session.commit()
    return volunteer

def db_update_volunteer(id, db_model, first_name=None, last_name=None, phone_number=None):
    try:
        volunteer = get_volunteer_by_id(id)
    except NoRecordFound:
        raise
    if first_name:  # TODO: methods to validate first_name
        volunteer.first_name = first_name
    if last_name:  # TODO: methods to validate last_name
        volunteer.last_name = last_name
    if phone_number:  # TODO: methods to validate phone_number
        volunteer.phone_number = phone_number
    db_model.session.flush()
    db_model.session.commit()
    return volunteer

def get_all_volunteers():
    all_volunteers = Volunteer.query.all()
    return models_list_to_dict(all_volunteers)


def get_volunteer_by(param_name, param_value, connection):
    query = f"SELECT * FROM volunteers WHERE {param_name}={param_value}"
    volunteers_by_param = execute_query(connection, query)
    return volunteers_by_param


def get_volunteer_by_id(volunteer_id: int):
    try:
        volunteer = Volunteer.query.filter_by(volunteer_id=volunteer_id).one()
    except exc.NoResultFound as e:
        #     TO_DO: Logger with original error message logger.warning(e.message)
        raise NoRecordFound
    return volunteer

# new_volunteer_attributes = {'first_name': 'Mateuszek'}
# volunteer = get_volunteer_by_id(12)
# print(volunteer.first_name)
# print(volunteer.last_name)
# volunteer_dict = volunteer.__dict__
# for attr_name, attr_value in new_volunteer_attributes.items():
#     if attr_value:
#         volunteer_dict[attr_name] = attr_value
# volunteer = volunteer_dict
# print(volunteer.first_name)
# print(volunteer.last_name)
# Funkcja niech wyrzuca bledy np. raise valueError kiedy tabela jest pusta lub nie istnieje lub gdy nie udalo sie polaczenie z baza danych.
# Chociaz polaczenie z baza danych juz jest sprawdzane w create connection try/except.
# Controller powinien przechwycic te bledy i przekazac klientowi numer bledu np. 405 wraz z trescia np. pusta baza danych etc.
# Dzieki temu jesli w db_handler cos sie skopie to po prostu wypycha blad do controllera a controller ten blad odpowiednio obrobi i wyrzuci do klienta.
