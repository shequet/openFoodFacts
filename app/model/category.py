#! /usr/bin/env python3
# coding: utf-8
""" Category class """
from app.database import Database
from constant import LIMIT_CATEGORY_ITEMS


class Category(Database):
    """ Category class"""

    def __init__(self):
        super().__init__()

    def add(self, name):
        """ Add category"""

        category = self.search_by_name(name)

        if category is None:
            self.execute("""
            INSERT INTO
                categories(
                    name
                    ) VALUES (
                    %s
                    )
            """, (name, ))
            return self.search_by_name(name)[0]
        else:
            return category[0]

    def search_by_name(self, name):
        """ Search category by name """

        return self.fetch_one("""
        SELECT
            *
        FROM
            categories
        WHERE
            name=%s;
        """, (name,))

    def show(self):
        """ Show categories """

        return self.fetch_all("""
        SELECT
            id,
            name
        FROM
            categories
        ORDER BY
            id ASC
        LIMIT {limit}
        """.format(limit=LIMIT_CATEGORY_ITEMS, ))
