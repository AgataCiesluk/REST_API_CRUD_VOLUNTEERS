from logger import Logger

if __name__ == "__main__":
    logger = Logger("name", "DEBUG", "DEBUG", "logs").logger
    logger.debug("this is a debug message")
