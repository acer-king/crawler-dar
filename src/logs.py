import logging
import os
import sys


log_level = os.getenv("LOG_LEVEL", "")
log_file_path = os.getenv("LOG_PATH", "") + os.getenv("LOG_FILE_NAME", "")

if log_level == "INFO":
    log_level = logging.INFO
elif log_level == "DEBUG":
    log_level = logging.DEBUG
elif log_level == "WARNING":
    log_level = logging.WARN
else:
    log_level = logging.INFO

if log_file_path == "":
    logging.basicConfig(
        format='[%(asctime)s],%(msecs)d %(name)s %(levelname)s [%(filename)s:%(lineno)s - %(funcName)20s() ] %('
               'message)s',
        datefmt="%m/%d/%Y %I:%M:%S %p",
        level=log_level
    )
else:
    logging.basicConfig(
        filename=log_file_path,
        filemode='w',
        format='[%(asctime)s],%(msecs)d %(name)s %(levelname)s [%(filename)s:%(lineno)s - %(funcName)20s() ] %('
               'message)s',
        datefmt="%m/%d/%Y %I:%M:%S %p",
        level=log_level
    )

sys.stdout.write = logging.info
