"""This is module with functions and their exemplary implementation that includes database db_volunteer creation,
 as well as methods needed to create volunteers table with exemplary data.

 This module doesn't have to be used if db_volunteer already exist and contains volunteer table with exemplary rows."""
# import logging
#
# import psycopg2
# from dotenv import dotenv_values
# from psycopg2 import OperationalError
#
# from database.db_config import DB_CONNECTION_ARGS
#
# config = dotenv_values("../.env")
#
#
# def create_connection(db_name, db_user, db_password, db_host, db_port):
#     connection = None
#     try:
#         connection = psycopg2.connect(
#             database=db_name,
#             user=db_user,
#             password=db_password,
#             host=db_host,
#             port=db_port,
#         )
#         print("Connection to PostgreSQL DB successful")
#     except OperationalError as e:
#         print(f"The error '{e}' occurred")
#     return connection
#
#
# def execute_query(connection, query, insert_data=None):
#     connection.autocommit = True
#     cursor = connection.cursor()
#     try:
#         if insert_data:
#             cursor.execute(query, insert_data)
#         else:
#             cursor.execute(query)
#             query_result = cursor.fetchall()
#             if query_result:
#                 return query_result
#         print("Query executed successfully")
#     except OperationalError as e:
#         print(f"The error '{e}' occurred")
#     finally:
#         cursor.close()
#         connection.close()
#
#
# def insert_data_into_volunteers_table(data: list):
#     if not data:
#         raise ValueError("Data list should not be empty.")
#     connection = create_connection(*DB_CONNECTION_ARGS)
#     data_records = ", ".join(["%s"] * len(data))
#     insert_query = (
#         f"INSERT INTO volunteers (first_name, last_name, phone_number) VALUES ({data_records})"
#     )
#     execute_query(connection, insert_query, data)
#     success_info = f"Data inserted into volunteers table in DB db_volunteers."
#     logging.info(success_info)
#     print(success_info)
#
#
# ### Create DB db_volunteers if not exist ####
# def create_db(db_name):
#     conn_postgres = create_connection(
#         "postgres",
#         config.get("DB_USER"),
#         config.get("DB_PASSWORD"),
#         config.get("DB_HOST"),
#         config.get("DB_PORT"))
#     execute_query(conn_postgres, f"CREATE DATABASE {db_name}")
#     conn_postgres.close()
#     success_info = f"DB {db_name} created."
#     logging.info(success_info)
#     print(success_info)
#
#
# create_db(config.get('DB_NAME'))
#
# ## Connect to DB db_volunteers if this DB exists ###
# conn_volunteers = create_connection(*DB_CONNECTION_ARGS)
# conn_volunteers.close()
#
# ## Create volunteers table in DB db_volunteers if this table doesn't exist ###
# conn_volunteers = create_connection(*DB_CONNECTION_ARGS)
# create_volunteers_table_query = """
# CREATE TABLE IF NOT EXISTS volunteers (
#   volunteer_id SERIAL PRIMARY KEY,
#   first_name VARCHAR (50) NOT NULL,
#   last_name VARCHAR (50) NOT NULL,
#   phone_number VARCHAR (12) UNIQUE,
# )
# """
#
# execute_query(conn_volunteers, create_volunteers_table_query)
#
# ## Add exemplary volunteers to voluneetrs table in DB db_volunteers ###
# volunteers = [
#     ("Agata", "Christie", "555-999-222"),
#     ("James", "Smith", "555-666-222"),
#     ("Leila", "Smither", "555-777-225"),
#     ("Brigitte", "Jones", "666-666-222"),
# ]
# insert_data_into_volunteers_table(volunteers)
