
# Script Python permettant de trouver des produits de substitution à partir de vos produits avec un Nutri Score bien meilleur.

### Pré requis avant installation
Le script fonctionne sous Windows, Mac et Linux, cependant il est nécessaire d'avoir installé Python en version 3 ainsi que le moteur de base de données MySQL.

### Installation
- Il est préférable de créer un environnement virtuel python3 -m virtualenv env
- Activez votre environnement virtuel ./env/bin/activate
- Installez les dépendances pip install -r requirements.txt
- Modifier vos variables d'environnement afin de configurer la connexion à votre serveur MySQL

|  Variables d'environnement | Description  | Exemple  |
|---|---|---|
|  DATABASE_HOST |  Nom ou adresse IP | 127.0.0.1 |
|  DATABASE_PORT |  Numéro du port | 3306 |
|  DATABASE_USER |  Nom du compte utilisateur | root |
|  DATABASE_PASSWORD |  Mot de passe | 123456 |
|  DATABASE_NAME |  Nom de la base de données | openfoodfact |

- Exécutez le script SQL permettant de créer la base de données ainsi que les tables, fichier à la racine du projet ``create_database.sql``

#### Paramétrage avant importation des données
Vous pouvez configurer les catégories à importer depuis l'API d'openFoodFacts depuis le fichier ``constant.py``

|  Constante | Description  | Exemple  |
|---|---|---|
| OPENFOODFACTS_URL  |  URL de l'API d'openFoodFacts | 'https://fr.openfoodfacts.org' |
| OPENFOODFACTS_PAGE_SIZE  |  Nombre de produit importé pour chaque requête sur l'API | 100 |
| OPENFOODFACTS_CATEGORIES  | Noms des catégories à importer | ('sodas-au-cola', 'cremes-fraiches', ) |
| LIMIT_CATEGORY_ITEMS  |  Nombre de catégories maximum | 10 |
| LIMIT_PRODUCT_ITEMS  |  Nombre de produits maximum | 10 |


#### Importation des données depuis OpenFoodFacts
Pour importer les produits depuis l'API d'OpenFoodsFact dans la base de données MySQL il est nécessaire d'exécuter le script Python :

``python import_openfoodfacts.py``

Affichage du nombre de pages ainsi que du nombre de produits importés :
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

## Utilisation du script principal

Le script principal est à lancer avec la commande

``python main.py``

Vous pouvez choisir entre les choix suivants :

1) Quel aliment souhaitez-vous remplacer ?
2) Retrouver mes aliments substitués.


### Choix 1 : Quel aliment souhaitez-vous remplacer ?

#### Affichage des catégories de produits :
```
+--------+-----------------------------+
| Numéro | Catégorie                   |
+--------+-----------------------------+
| 1      | Produits à tartiner         |
| 2      | Sodas                       |
| 3      | Pizza                       |
+--------+-----------------------------+
Sélectionnez une catégorie:
```
Sélection : `` 1 + [Entrer]``

#### Affichage des produits de la catégorie sélectionnée (_1 - Produits à tartiner_):

```
+----+-------------+---------------------------------------------------------+
| Id | Nutri Score | Nom du produit                                          |
+----+-------------+---------------------------------------------------------+
| 1  | E           | Pâte à tartiner 750 g                                   |
| 2  | D           | Pâte à tartiner 350 g                                   |
| 3  | E           | Nutella 400 g                                           |
+----+-------------+---------------------------------------------------------+
Sélectionnez un aliment:
```

Sélection : `` 3 + [Entrer]``

#### Affichage du produit sélectionné ainsi que le produit de substitution (_3 - Nutella 400 g_):

```
+---------------------------+-----+-------------+--------------------------+-------------------------------+-------------+----------------------------------------------------+
| Type                      | Id  | Nutri Score | Marque(s)                | Nom du produit                | Boutique(s) | lien OpenFoodFacts                                 |
+---------------------------+-----+-------------+--------------------------+-------------------------------+-------------+----------------------------------------------------+
| Votre produit :           | 3   | D           | Carrefour, Carrefour Bio | Pâte à tartiner               | Carrefour   | https://fr.openfoodfacts.org/produit/3560070472888 |
| Produit de substitution : | 499 | B           | Weider                   | Nutproteinchocospread, Chunky |             | https://fr.openfoodfacts.org/produit/8414192310168 |
+---------------------------+-----+-------------+--------------------------+-------------------------------+-------------+----------------------------------------------------+
Voulez-vous enregistrer le substitut ?
1) Enregsitrer
*) Autre touche retour au menu de départ
```

Sélection : `` 1 + [Entrer]``

#### Enregistrement du produit de substitution en base de données:

### Choix 2 : Retrouver mes aliments substitués

```
+---------------------------+-----+-------------+-----------+-----------------------+-----------------+----------------------------------------------------+
| Type                      | Id  | Nutri Score | Marque(s) | Nom du produit        | Boutique(s)     | lien OpenFoodFacts                                 |
+---------------------------+-----+-------------+-----------+-----------------------+-----------------+----------------------------------------------------+
| Votre produit :           | 1   | C           | Pepsi     | Pepsi                 | Magasins U, kfc | https://fr.openfoodfacts.org/produit/3502110008329 |
| Produit de substitution : | 516 | B           | Coca-Cola | Coca-cola zéro cherry |                 | https://fr.openfoodfacts.org/produit/5449000223586 |
+---------------------------+-----+-------------+-----------+-----------------------+-----------------+----------------------------------------------------+

+---------------------------+-----+-------------+--------------+------------------------------+--------------+----------------------------------------------------+
| Type                      | Id  | Nutri Score | Marque(s)    | Nom du produit               | Boutique(s)  | lien OpenFoodFacts                                 |
+---------------------------+-----+-------------+--------------+------------------------------+--------------+----------------------------------------------------+
| Votre produit :           | 617 | D           | Netto        | Creme fraiche epaisse        |              | https://fr.openfoodfacts.org/produit/3250392849474 |
| Produit de substitution : | 660 | B           | Leader Price | Crème fraîche épaisse légère | Leader Price | https://fr.openfoodfacts.org/produit/3263859753719 |
+---------------------------+-----+-------------+--------------+------------------------------+--------------+----------------------------------------------------+

1) Quel aliment souhaitez-vous remplacer ?
2) Retrouver mes aliments substitués.
```