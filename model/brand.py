#! /usr/bin/env python3
# coding: utf-8
""" Brand class """
from model.database import Database


class Brand(Database):
    """ Brand class"""

    def __init__(self):
        super().__init__()

    def add(self, name):
        """ Add brand"""

        brand = self.search_by_name(name)

        if brand is None:
            self.execute("""
            INSERT INTO
                brands(
                    name
                    )VALUES (
                    %s
                    )
            """, (name, ))
            return self.search_by_name(name)[0]
        else:
            return brand[0]

    def search_by_name(self, name):
        """ Search brand by name"""

        return self.fetch_one("""
        SELECT
            *
        FROM
            brands
        WHERE
            name=%s;
        """, (name,))

    def show(self):
        """ Show brands"""

        return self.fetch_all("""
        SELECT
            id,
            name
        FROM
            brands
        ORDER BY
            name ASC
        """)
