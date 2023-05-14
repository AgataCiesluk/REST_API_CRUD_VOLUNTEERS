from app.database.db_handler import get_all_volunteers, create_connection
from app.database.db_config import DB_CONNECTION_ARGS



# @app.route('/volunteers')
# def get_all_volunteers():
#     all_volunteers = get_all_volunteers(create_connection(*DB_CONNECTION_ARGS))
#     return {'volunteers': all_volunteers}

print(get_all_volunteers(create_connection(*DB_CONNECTION_ARGS)))
print(DB_CONNECTION_ARGS)
