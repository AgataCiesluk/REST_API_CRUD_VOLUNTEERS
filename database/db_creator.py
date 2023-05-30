"""This is module with functions and their exemplary implementation that includes database db_volunteer creation,
 as well as methods needed to create volunteers table with exemplary data.

 This module doesn't have to be used if db_volunteer already exist and contains volunteer table with exemplary rows."""

from dotenv import dotenv_values

config = dotenv_values("../.env")


#### Create DB db_volunteers if not exist ####
# def create_db(db_name):
#     conn_postgres = create_connection(
#         "postgres",
#         config.get("DB_USER"),
#         config.get("DB_PASSWORD"),
#         config.get("DB_HOST"),
#         config.get("DB_PORT"))
#     execute_query_without_return(conn_postgres, f"CREATE DATABASE {db_name}")
#     conn_postgres.close()
#     success_info = f"DB {db_name} created."
#     logging.info(success_info)
#     print(success_info)
#
#
# create_db(config.get('DB_NAME'))



### Connect to DB db_volunteers if this DB exists ###
# conn_volunteers = create_connection(*DB_CONNECTION_ARGS)
# conn_volunteers.close()


### Create volunteers table in DB db_volunteers if this table doesn't exist ###
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


### Add exemplary volunteers to voluneetrs table in DB db_volunteers ###
# volunteers = [
#     ("Agata", "Christie", "555-999-222"),
#     ("James", "Smith", "555-666-222"),
#     ("Leila", "Smither", "555-777-225"),
#     ("Brigitte", "Jones", "666-666-222"),
# ]
# insert_data_into_volunteers_table(volunteers)
