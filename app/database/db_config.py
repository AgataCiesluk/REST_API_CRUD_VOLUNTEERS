from dotenv import dotenv_values

config = dotenv_values("../../env/.env")
DB_CONNECTION_ARGS = [
    config.get("DB_NAME"),
    config.get("DB_USER"),
    config.get("DB_PASSWORD"),
    config.get("DB_HOST"),
    config.get("DB_PORT")]
