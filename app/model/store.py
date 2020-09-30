#! /usr/bin/env python3
# coding: utf-8
""" Store class """
from app.database import Database


class Store(Database):
    """ Store class"""

    def __init__(self):
        super().__init__()

    def add(self, name):
        """ Add store """
        store = self.search_by_name(name)

        if store is None:
            self.execute("""
            INSERT INTO
                stores(
                    name
                ) VALUES (
                    %s
                )
            """, (name, ))
            return self.search_by_name(name)[0]
        else:
            return store[0]

    def search_by_name(self, name):
        """ Search store by name """

        return self.fetch_one("""
        SELECT
            *
        FROM
            stores
        WHERE
            name=%s
        """, (name,))

    def show(self):
        """ Show stores"""

        return self.fetch_all("""
        SELECT
            id,
            name
        FROM
            stores
        ORDER BY
            name ASC
        """)
