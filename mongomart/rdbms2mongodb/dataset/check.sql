use mongomart;
drop table reviews;

-- -----------------------------------------------------
-- Table `mongomart`.`reviews`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mongomart`.`reviews` (
  `id` INT NOT NULL AUTO_INCREMENT COMMENT '	',
  `name` VARCHAR(45) NULL,
  `date` DATETIME NULL,
  `comment` TEXT NULL,
  `stars` INT ZEROFILL NULL,
  `items_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_reviews_items1_idx` (`items_id` ASC),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC),
  CONSTRAINT `fk_reviews_items1`
    FOREIGN KEY (`items_id`)
    REFERENCES `mongomart`.`items` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SELECT COUNT(1) AS "Number of Items" FROM `mongomart`.`items`;
SELECT "23" AS "Expected Number of Items";

SELECT COUNT(1) AS "Number of Stores" FROM `mongomart`.`stores`;
SELECT "116" AS "Expected Number of Stores";

SELECT COUNT(1) AS "Number of Addresses" FROM `mongomart`.`addresses`;
SELECT "116" AS "Expected Number of Addresses";
