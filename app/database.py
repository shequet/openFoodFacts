#! /usr/bin/env python3
# coding: utf-8
""" Database class """
import mysql.connector
import os


class Database:
    """ Database class"""

    def __init__(self):
        self.conn = mysql.connector.connect(
            host=os.environ.get('DATABASE_HOST', '127.0.0.1'),
            user=os.environ.get('DATABASE_USER', 'root'),
            port=os.environ.get('DATABASE_PORT', 3306),
            password='123456',
            database=os.environ.get('DATABASE_NAME', 'openfoodfact')
        )
        self.conn.autocommit = True
        self.cursor = self.conn.cursor()

    def execute(self, query, params=()):
        """ Execute query in database"""

        self.cursor.execute(query, params)

    def fetch_one(self, query, params=()):
        """ Fetch one record """

        self.execute(query, params)
        return self.cursor.fetchone()

    def fetch_all(self, query, params=()):
        """ Fetch all record """

        self.execute(query, params)
        return self.cursor.fetchall()
