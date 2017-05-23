-- MySQL dump 10.13  Distrib 5.7.17, for macos10.12 (x86_64)
--
-- Host: 127.0.0.1    Database: mongomart
-- ------------------------------------------------------
-- Server version	5.7.18

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `items_has_categories`
--

DROP TABLE IF EXISTS `items_has_categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `items_has_categories` (
  `items_id` int(11) NOT NULL,
  `items_category` varchar(45) NOT NULL,
  `categories_name` varchar(45) NOT NULL,
  PRIMARY KEY (`items_id`,`items_category`,`categories_name`),
  KEY `fk_items_has_categories_categories1_idx` (`categories_name`),
  KEY `fk_items_has_categories_items1_idx` (`items_id`,`items_category`),
  CONSTRAINT `fk_items_has_categories_categories1` FOREIGN KEY (`categories_name`) REFERENCES `categories` (`name`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_items_has_categories_items1` FOREIGN KEY (`items_id`, `items_category`) REFERENCES `old_items` (`id`, `category`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `items_has_categories`
--

LOCK TABLES `items_has_categories` WRITE;
/*!40000 ALTER TABLE `items_has_categories` DISABLE KEYS */;
INSERT INTO `items_has_categories` VALUES (1,'Apparel','Apparel'),(4,'Apparel','Apparel'),(5,'Apparel','Apparel'),(10,'Apparel','Apparel'),(20,'Apparel','Apparel'),(23,'Apparel','Apparel'),(11,'Books','Books'),(15,'Books','Books'),(19,'Books','Books'),(13,'Electronics','Electronics'),(14,'Electronics','Electronics'),(21,'Electronics','Electronics'),(2,'Kitchen','Kitchen'),(7,'Kitchen','Kitchen'),(22,'Kitchen','Kitchen'),(8,'Office','Office'),(9,'Office','Office'),(12,'Stickers','Stickers'),(16,'Stickers','Stickers'),(3,'Swag','Swag'),(6,'Swag','Swag'),(17,'Umbrellas','Umbrellas'),(18,'Umbrellas','Umbrellas');
/*!40000 ALTER TABLE `items_has_categories` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-05-17 18:50:11
