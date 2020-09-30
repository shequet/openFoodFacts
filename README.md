
# Python script to find substitute products from your products with a much better Nutri Score.

### Prerequisites before installation
The script works on Windows, Mac and Linux, however it is necessary to have Python version 3 installed as well as the MySQL database engine.

### Installation
- It is better to create a virtual environment ``python3 -m virtualenv env``
- Activate your virtual environment ``./env/bin/activate``
- Install dependencies ``pip install -r requirements.txt``
- Modify your environment variables to configure the connection to your MySQL server

|  Environment variables | Description  | Example  |
|---|---|---|
|  DATABASE_HOST |  Name or IP address | 127.0.0.1 |
|  DATABASE_PORT |  Port number | 3306 |
|  DATABASE_USER |  User account name | root |
|  DATABASE_PASSWORD |  Password | 123456 |
|  DATABASE_NAME |  Name of the database | openfoodfact |

- Run the SQL script used to create the database as well as the tables, SQL file ``install/create_database.sql``

#### Settings before data import
You can configure the categories to import from the openFoodFacts API from the file ``constant.py``

|  Constant | Description  | Example  |
|---|---|---|
| OPENFOODFACTS_URL  |  OpenFoodFacts API URL | 'https://fr.openfoodfacts.org' |
| OPENFOODFACTS_PAGE_SIZE  |  Number of products imported for each API request | 100 |
| OPENFOODFACTS_CATEGORIES  | Names of categories to import | ('sodas-au-cola', 'cremes-fraiches', ) |
| LIMIT_CATEGORY_ITEMS  |  Maximum number of categories | 10 |
| LIMIT_PRODUCT_ITEMS  |  Maximum number of products | 10 |


#### Importing data from OpenFoodFacts
To import the products from the OpenFoodsFact API into the MySQL database it is necessary to run the Pytho script :

``python import_openfoodfacts.py``

Display of the number of pages as well as the number of imported products :
```
-----Page:[1]-----Total products:[100]-----
-----Page:[2]-----Total products:[200]-----
-----Page:[3]-----Total products:[300]-----
-----Page:[4]-----Total products:[400]-----
-----Page:[5]-----Total products:[500]-----
-----Page:[6]-----Total products:[600]-----
-----Page:[7]-----Total products:[700]-----
-----Page:[8]-----Total products:[773]-----
-----Page:[1]-----Total products:[873]-----
-----Page:[2]-----Total products:[973]-----
-----Page:[3]-----Total products:[1073]-----
-----Page:[4]-----Total products:[1120]-----
```

## Using the main script

The main script is to be started with the command

``python main.py``

You can choose between the following choices :

1) What food do you want to replace ?
2) Find my substitute foods.


### Choice 1: What food do you want to replace ?

#### Display of product categories :
```
+--------+-----------------------------+
| Number | Category                    |
+--------+-----------------------------+
| 1      | Produits à tartiner         |
| 2      | Sodas                       |
| 3      | Pizza                       |
+--------+-----------------------------+
Select a category:
```
Selection : `` 1 + [Entrer]``

#### Display of products of the selected category (_1 - Produits à tartiner_):

```
+----+-------------+---------------------------------------------------------+
| Id | Nutri Score | Produit Name                                            |
+----+-------------+---------------------------------------------------------+
| 1  | E           | Pâte à tartiner 750 g                                   |
| 2  | D           | Pâte à tartiner 350 g                                   |
| 3  | E           | Nutella 400 g                                           |
+----+-------------+---------------------------------------------------------+
Select a food:
```

Selection : `` 3 + [Entrer]``

#### Display of the selected product as well as the substitute product (_3 - Nutella 400 g_):

```
+---------------------------+-----+-------------+--------------------------+-------------------------------+-------------+----------------------------------------------------+
| Type                      | Id  | Nutri Score | Brand(s)                 | Produit Name                  | Shop(s)     | OpenFoodFacts Link                                 |
+---------------------------+-----+-------------+--------------------------+-------------------------------+-------------+----------------------------------------------------+
| Votre produit :           | 3   | D           | Carrefour, Carrefour Bio | Pâte à tartiner               | Carrefour   | https://fr.openfoodfacts.org/produit/3560070472888 |
| Produit de substitution : | 499 | B           | Weider                   | Nutproteinchocospread, Chunky |             | https://fr.openfoodfacts.org/produit/8414192310168 |
+---------------------------+-----+-------------+--------------------------+-------------------------------+-------------+----------------------------------------------------+
Do you want to save the substitute ?
1) Save
*) Other key back to the start menu
```

Selection : `` 1 + [Entrer]``

#### Registration of the replacement product in the database :

### Choice 2: Find my substituted foods

```
+---------------------------+-----+-------------+-----------+-----------------------+-----------------+----------------------------------------------------+
| Type                      | Id  | Nutri Score | Brand(s)  | Product Name          | Shop(s)         | OpenFoodFacts Link                                 |
+---------------------------+-----+-------------+-----------+-----------------------+-----------------+----------------------------------------------------+
| Votre produit :           | 1   | C           | Pepsi     | Pepsi                 | Magasins U, kfc | https://fr.openfoodfacts.org/produit/3502110008329 |
| Produit de substitution : | 516 | B           | Coca-Cola | Coca-cola zéro cherry |                 | https://fr.openfoodfacts.org/produit/5449000223586 |
+---------------------------+-----+-------------+-----------+-----------------------+-----------------+----------------------------------------------------+

+---------------------------+-----+-------------+--------------+------------------------------+--------------+----------------------------------------------------+
| Type                      | Id  | Nutri Score | Brand(s)     | Product Name                 | Shop(s)      | OpenFoodFacts Link                                 |
+---------------------------+-----+-------------+--------------+------------------------------+--------------+----------------------------------------------------+
| Votre produit :           | 617 | D           | Netto        | Creme fraiche epaisse        |              | https://fr.openfoodfacts.org/produit/3250392849474 |
| Produit de substitution : | 660 | B           | Leader Price | Crème fraîche épaisse légère | Leader Price | https://fr.openfoodfacts.org/produit/3263859753719 |
+---------------------------+-----+-------------+--------------+------------------------------+--------------+----------------------------------------------------+

1) What food do you want to replace ?
2) Find my substitute foods.
```