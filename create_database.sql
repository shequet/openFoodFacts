
-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema openfoodfact
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema openfoodfact
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `openfoodfact` DEFAULT CHARACTER SET utf8 ;
USE `openfoodfact` ;

-- -----------------------------------------------------
-- Table `openfoodfact`.`brands`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `openfoodfact`.`brands` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(1024) NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `name` (`name` ASC) )
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `openfoodfact`.`categories`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `openfoodfact`.`categories` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(1024) NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `name` (`name` ASC) )
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `openfoodfact`.`products`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `openfoodfact`.`products` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `code` VARCHAR(255) NOT NULL,
  `name` VARCHAR(255) NOT NULL,
  `quantity` VARCHAR(255) NULL DEFAULT NULL,
  `link` VARCHAR(2048) NULL DEFAULT NULL,
  `nutriscore` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `code` (`code` ASC) ,
  INDEX `name` (`name` ASC) )
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `openfoodfact`.`product_brands`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `openfoodfact`.`product_brands` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `product_id` INT(11) NULL DEFAULT NULL,
  `brand_id` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `product_brands` (`product_id` ASC, `brand_id` ASC) ,
  INDEX `product_id` (`product_id` ASC) ,
  INDEX `brand_id` (`brand_id` ASC) ,
  CONSTRAINT `product_brands:brand_id`
    FOREIGN KEY (`brand_id`)
    REFERENCES `openfoodfact`.`brands` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `product_brands:product`
    FOREIGN KEY (`product_id`)
    REFERENCES `openfoodfact`.`products` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `openfoodfact`.`product_categories`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `openfoodfact`.`product_categories` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `product_id` INT(11) NULL DEFAULT NULL,
  `category_id` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `product_id` (`product_id` ASC) ,
  INDEX `category_id` (`category_id` ASC) ,
  CONSTRAINT `fk_product_categories:category_id`
    FOREIGN KEY (`category_id`)
    REFERENCES `openfoodfact`.`categories` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_product_categories:product_id`
    FOREIGN KEY (`product_id`)
    REFERENCES `openfoodfact`.`products` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `openfoodfact`.`stores`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `openfoodfact`.`stores` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(1024) NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `name` (`name` ASC) )
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `openfoodfact`.`product_stores`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `openfoodfact`.`product_stores` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `product_id` INT(11) NULL DEFAULT NULL,
  `store_id` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `product_stores` (`product_id` ASC, `store_id` ASC) ,
  INDEX `product_id` (`product_id` ASC) ,
  INDEX `store_id` (`store_id` ASC) ,
  CONSTRAINT `product_stores:brand_id`
    FOREIGN KEY (`store_id`)
    REFERENCES `openfoodfact`.`stores` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `product_stores:product`
    FOREIGN KEY (`product_id`)
    REFERENCES `openfoodfact`.`products` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `openfoodfact`.`product_substitute`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `openfoodfact`.`product_substitute` (
  `id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `product_id` INT(11) NULL DEFAULT NULL,
  `substitute_product_id` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id` (`id` ASC) ,
  INDEX `product_id` (`product_id` ASC) ,
  INDEX `substitute_product_id` (`substitute_product_id` ASC) ,
  CONSTRAINT `product_substitute:product_id`
    FOREIGN KEY (`product_id`)
    REFERENCES `openfoodfact`.`products` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `product_substitute:substitute_product_id`
    FOREIGN KEY (`substitute_product_id`)
    REFERENCES `openfoodfact`.`products` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
DEFAULT CHARACTER SET = utf8;
