from argparse import ArgumentParser
from os import getenv
from pathlib import Path

from logger import Logger


def parser():
    parser = ArgumentParser(allow_abbrev=False)

    parser.add_argument(
        "--console-log-level",
        dest="console_log_level",
        default=getenv("CONSOLE_LOG_LEVEL", "DEBUG"),
        help="Console logging level.",
        type=str,
    )
    parser.add_argument(
        "--file-log-level",
        dest="file_log_level",
        default=getenv("FILE_LOG_LEVEL", "INFO"),
        help="File logging level.",
        type=str,
    )
    parser.add_argument(
        "--file-log-dir",
        dest="file_log_dir",
        default=getenv("FILE_LOG_DIR", str(Path().absolute() / "logs")),
        help="A directory for logs storage.",
        type=str,
    )

    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parser()

    logger = Logger(
        name=__name__,
        console_log_level=args.console_log_level,
        file_log_level=args.file_log_level,
        file_log_dir=args.file_log_dir,
    ).logger

    logger.debug("this is a debug message")
    logger.info("this is INFO")






