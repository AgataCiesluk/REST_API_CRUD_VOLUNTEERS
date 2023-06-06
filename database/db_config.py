from dotenv import dotenv_values

config = dotenv_values()
DB_CONNECTION_ARGS = [
    config.get("DB_NAME"),
    config.get("DB_USER"),
    config.get("DB_PASSWORD"),
    config.get("DB_HOST"),
    config.get("DB_PORT")]

DB_CONNECTION_PARAMS = {
    "DB_NAME": config.get("DB_NAME"),
    "DB_USER": config.get("DB_USER"),
    "DB_PASSWORD": config.get("DB_PASSWORD"),
    "DB_HOST": config.get("DB_HOST"),
    "DB_PORT": config.get("DB_PORT")
}