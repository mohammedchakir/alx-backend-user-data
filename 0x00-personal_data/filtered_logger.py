#!/usr/bin/env python3
"""
This module provides a function to obfuscate specified fields in a log message,
a RedactingFormatter class to format log records with obfuscated values,
and a get_logger function to configure a logger with specific settings.
"""

import os
import re
from os import environ
import logging
from typing import List, Tuple
import mysql.connector
from mysql.connector.connection import MySQLConnection


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Obfuscate specified fields in the log message.

    :param fields: List of strings representing fields to obfuscate.
    :param redaction: String representing the replacement text.
    :param message: The log message.
    :param separator: The field separator in the log message.
    :return: The obfuscated log message.
    """
    pattern = '|'.join(f'(?<={field}=)[^{separator}]+' for field in fields)
    return re.sub(pattern, redaction, message)


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class for filtering sensitive information from logs.
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initialize the formatter with fields to redact.

        :param fields: List of strings representing fields to obfuscate.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record, obfuscating specified fields.

        :param record: The log record to format.
        :return: The formatted log record as a string.
        """
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.msg, self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


PII_FIELDS: Tuple[str, ...] = ("name", "email", "phone", "ssn", "password")


def get_logger() -> logging.Logger:
    """
    Create and configure a logger named 'user_data' to log obfuscated messages.

    :return: Configured logger object.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=list(PII_FIELDS))
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    return logger


def get_db() -> MySQLConnection:
    """
    Connect to a secure MySQL database using credentials from
    environment variables.

    :return: A MySQLConnection object.
    """
    username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    database = os.getenv('PERSONAL_DATA_DB_NAME')

    return mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=database
    )


def main():
    """
    Main function that retrieves all rows from the users table and
    logs each row with sensitive fields obfuscated.
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    field_names = [i[0] for i in cursor.description]

    logger = get_logger()

    for row in cursor:
        str_row = ''.join(f'{f}={str(r)}; ' for r, f in zip(row, field_names))
        logger.info(str_row.strip())

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
