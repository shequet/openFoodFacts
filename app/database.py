#! /usr/bin/env python3
# coding: utf-8
""" Database class """
import mysql.connector
import os


class Database:
    """ Database class"""

    def __init__(self):
        self.connect()

    def connect(self):
        """ Connection in database"""

        self.conn = mysql.connector.connect(
            host=os.environ.get('DATABASE_HOST', '127.0.0.1'),
            user=os.environ.get('DATABASE_USER', 'root'),
            port=os.environ.get('DATABASE_PORT', 3306),
            password='123456',
            database=os.environ.get('DATABASE_NAME', 'openfoodfact')
        )

    def execute(self, query, params=()):
        """ Execute query in database"""

        cursor = self.conn.cursor()
        cursor.execute(query, params)
        self.conn.commit()
        cursor.close()

    def fetch_one(self, query, params=()):
        """ Fetch one record """

        cursor = self.conn.cursor()
        cursor.execute(query, params)
        row = cursor.fetchone()
        cursor.close()
        return row

    def fetch_all(self, query, params=()):
        """ Fetch all record """

        cursor = self.conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        cursor.close()
        return rows
