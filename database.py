#! /usr/bin/env python3
# coding: utf-8
""" Database class """
from psycopg2 import connect, extensions, errors, sql

from constant import DATABASE_HOST, DATABASE_NAME, DATABASE_PASSWORD, DATABASE_USER, DATABASE_PORT


class Database:
    """ Database class"""

    def __init__(self):
        self.connect()

    def connect(self):
        """ Connection in database"""
        self.conn = connect(
            user=DATABASE_USER,
            password=DATABASE_PASSWORD,
            host=DATABASE_HOST,
            port=DATABASE_PORT,
            dbname=DATABASE_NAME,
        )

        self.conn.set_isolation_level(extensions.ISOLATION_LEVEL_AUTOCOMMIT)

    def execute(self, query, params=()):
        """ Execute query in database"""
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        cursor.close()

    def fetch_one(self, query, params=()):
        """ Execute query in database"""
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        row = cursor.fetchone()
        cursor.close()
        return row

    def create_database(self):
        """ Create database in PostGreSql"""
        try:
            self.execute('CREATE DATABASE {database}'.format(database=DATABASE_NAME))
            return True
        except errors.DuplicateDatabase as e:
            return True

        return False


class Product(Database):
    """ Product class"""

    def __init__(self):
        super().__init__()
        self.create_table()
        self.category = Category()
        self.product_category = ProductCategory()

    def create_table(self):
        """ Create product table in database"""

        self.execute("""
        CREATE TABLE IF NOT EXISTS
            products (
                id SERIAL PRIMARY KEY,
                code varchar(255),
                name varchar(255),
                link varchar(2048),
                CONSTRAINT code UNIQUE (code)
                );""")

    def add(self, name, link, stores, brands, categories, code):
        product = self.search_by_code(code)
        if product is None:
            self.execute('INSERT INTO products(name, link, code) VALUES (%s, %s, %s)', (name, link, code, ))
            product = self.search_by_code(code)

        for category in categories.split(','):
            category_id = self.category.add(category.strip())
            self.product_category.add(product[0], category_id)

    def search_by_code(self, code):
        return self.fetch_one('SELECT * FROM products WHERE code=%s;', (code, ))


class Category(Database):
    """ Category class"""

    def __init__(self):
        super().__init__()
        self.create_table()

    def create_table(self):
        """ Create categories table in database"""

        self.execute("""
        CREATE TABLE IF NOT EXISTS
            categories (
                id SERIAL PRIMARY KEY,
                name varchar(1024),
                CONSTRAINT name UNIQUE (name)
                );""")

    def add(self, name):
        category = self.search_by_name(name)

        if category is None:
            self.execute('INSERT INTO categories(name) VALUES (%s)', (name, ))
            return self.search_by_name(name)[0]
        else:
            return category[0]

    def search_by_name(self, name):
        return self.fetch_one('SELECT * FROM categories WHERE name=%s;', (name,))


class ProductCategory(Database):
    """ product Category class"""

    def __init__(self):
        super().__init__()
        self.create_table()

    def create_table(self):
        """ Create product categories table in database"""

        self.execute("""
        CREATE TABLE IF NOT EXISTS
            product_categories (
                id SERIAL PRIMARY KEY,
                product_id integer,
                category_id integer,
                CONSTRAINT category_id FOREIGN KEY (category_id)
                    REFERENCES public.categories (id) MATCH SIMPLE
                    ON UPDATE NO ACTION
                    ON DELETE CASCADE
                    NOT VALID,
                CONSTRAINT product_id FOREIGN KEY (product_id)
                    REFERENCES public.products (id) MATCH SIMPLE
                    ON UPDATE NO ACTION
                    ON DELETE CASCADE
                    NOT VALID
                );""")

    def add(self, product_id, category_id):
        if self.search_by_product_category(product_id, category_id) is None:
            self.execute('INSERT INTO product_categories(product_id, category_id) VALUES (%s, %s)', (product_id, category_id, ))

    def search_by_product_category(self, product_id, category_id):
        return self.fetch_one('SELECT * FROM product_categories WHERE product_id=%s AND category_id=%s;', (product_id, category_id))
