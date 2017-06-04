-- MySQL dump 10.13  Distrib 5.7.18, for osx10.12 (x86_64)
--
-- Host: localhost    Database: mongomart
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
-- Table structure for table `stores`
--

DROP TABLE IF EXISTS `stores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `stores` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `distance_from_point` double DEFAULT NULL,
  `geo_id` int(11) DEFAULT NULL,
  `address_id` int(11) DEFAULT NULL,
  `store_id` varchar(100) NOT NULL,
  PRIMARY KEY (`id`,`store_id`),
  KEY `fk_stores_geo_idx` (`geo_id`),
  KEY `idx_name` (`name`) USING BTREE,
  KEY `fk_stores_Addresses1_idx` (`address_id`),
  CONSTRAINT `fk_stores_Addresses1` FOREIGN KEY (`address_id`) REFERENCES `addresses` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_stores_geo` FOREIGN KEY (`geo_id`) REFERENCES `geo` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=233 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stores`
--

LOCK TABLES `stores` WRITE;
/*!40000 ALTER TABLE `stores` DISABLE KEYS */;
INSERT INTO `stores` VALUES (117,'MongoMart Leominster',NULL,1,1,''),(118,'MongoMart - Auburn Mall',NULL,2,2,''),(119,'MongoMart Framingham',NULL,3,3,''),(120,'MongoMart - South Shore Plaza',NULL,4,4,''),(121,'MongoMart Braintree',NULL,5,5,''),(122,'MongoMart Cape Cod',NULL,6,6,''),(123,'MongoMart Attleboro',NULL,7,7,''),(124,'MongoMart Manchester',NULL,8,8,''),(125,'MongoMart Lebanon',NULL,9,9,''),(126,'MongoMart Portland',NULL,10,10,''),(127,'MongoMart Auburn',NULL,11,11,''),(128,'MongoMart Meriden',NULL,12,12,''),(129,'MongoMart - Meriden Mall',NULL,13,13,''),(130,'MongoMart Orange',NULL,14,14,''),(131,'MongoMart - Trumbull Shopping Park',NULL,15,15,''),(132,'MongoMart West Paterson',NULL,16,16,''),(133,'MongoMart Howell',NULL,17,17,''),(134,'MongoMart East Hanover',NULL,18,18,''),(135,'MongoMart Mount Laurel',NULL,19,19,''),(136,'MongoMart - Hawthorn Mall',NULL,20,20,''),(137,'MongoMart Bloomingdale',NULL,21,21,''),(138,'MongoMart Illinois Tollway - DeKalb Oasis',NULL,22,22,''),(139,'MongoMart - Fox Valley Center',NULL,23,23,''),(140,'MongoMart Kankakee',NULL,24,24,''),(141,'MongoMart Connecticut Turnpike - Milford Southbound',NULL,25,25,''),(142,'MongoMart - Cumberland Mall',NULL,26,26,''),(143,'MongoMart East Brunswick',NULL,27,27,''),(144,'MongoMart Upper West Side (62nd and Broadway)',NULL,28,28,''),(145,'MongoMart - Galleria at Crystal Run',NULL,29,29,''),(146,'MongoMart Long Island City',NULL,30,30,''),(147,'MongoMart - Green Acres Mall',NULL,31,31,''),(148,'MongoMart - Sunrise Mall',NULL,32,32,''),(149,'MongoMart Riverhead',NULL,33,33,''),(150,'MongoMart - Crossgates Mall',NULL,34,34,''),(151,'MongoMart - Hudson Valley Mall',NULL,35,35,''),(152,'MongoMart - Poughkeepsie Galleria',NULL,36,36,''),(153,'MongoMart - Destiny USA',NULL,37,37,''),(154,'MongoMart Middletown',NULL,38,38,''),(155,'MongoMart Watertown',NULL,39,39,''),(156,'MongoMart BUF - Buffalo Niagara International',NULL,40,40,''),(157,'MongoMart Henrietta',NULL,41,41,''),(158,'MongoMart So. Hills',NULL,42,42,''),(159,'MongoMart Monroeville',NULL,43,43,''),(160,'MongoMart - Millcreek Mall',NULL,44,44,''),(161,'MongoMart Muncy',NULL,45,45,''),(162,'MongoMart Pottstown',NULL,46,46,''),(163,'MongoMart Concord Pike',NULL,47,47,''),(164,'MongoMart Union Station - Washington D.C.',NULL,48,48,''),(165,'MongoMart - St Charles Towne Center',NULL,49,49,''),(166,'MongoMart Laurel',NULL,50,50,''),(167,'MongoMart Bowie',NULL,51,51,''),(168,'MongoMart - Westfield Montgomery',NULL,52,52,''),(169,'MongoMart - The Mall in Columbia',NULL,53,53,''),(170,'MongoMart - Valley Mall',NULL,54,54,''),(171,'MongoMart Baileys Crossroads',NULL,55,55,''),(172,'MongoMart Springfield',NULL,56,56,''),(173,'MongoMart Winchester',NULL,57,57,''),(174,'MongoMart Princess Anne',NULL,58,58,''),(175,'MongoMart - Southpark Mall',NULL,59,59,''),(176,'MongoMart Gastonia',NULL,60,60,''),(177,'MongoMart - Cross Creek Mall',NULL,61,61,''),(178,'MongoMart Alpharetta',NULL,62,62,''),(179,'MongoMart Acworth',NULL,63,63,''),(180,'MongoMart Douglasville',NULL,64,64,''),(181,'MongoMart ATL - Hartsfield Jackson Atlanta International Airport',NULL,65,65,''),(182,'MongoMart Buckhead',NULL,66,66,''),(183,'MongoMart Gainesville',NULL,67,67,''),(184,'MongoMart - Georgia Square Mall',NULL,68,68,''),(185,'MongoMart - Augusta Mall ',NULL,69,69,''),(186,'MongoMart The Avenues',NULL,70,70,''),(187,'MongoMart Panama City',NULL,71,71,''),(188,'MongoMart Destin',NULL,72,72,''),(189,'MongoMart MCO - Orlando International Airport',NULL,73,73,''),(190,'MongoMart MCO - Orlando International Airport',NULL,74,74,''),(191,'MongoMart MCO - Orlando International Airport',NULL,75,75,''),(192,'MongoMart MCO - Orlando International Airport',NULL,76,76,''),(193,'MongoMart - Melbourne Square Mall',NULL,77,77,''),(194,'MongoMart - Indian River Mall',NULL,78,78,''),(195,'MongoMart - 18 Biscayne',NULL,79,79,''),(196,'MongoMart FLL - Fort Lauderdale-Hollywood International Airport',NULL,80,80,''),(197,'MongoMart - Sawgrass Mills West',NULL,81,81,''),(198,'MongoMart Davie',NULL,82,82,''),(199,'MongoMart Wellington',NULL,83,83,''),(200,'MongoMart - Town Center at Boca Raton',NULL,84,84,''),(201,'MongoMart So. Tampa',NULL,85,85,''),(202,'MongoMart Davenport',NULL,86,86,''),(203,'MongoMart - Treasure Coast Square',NULL,87,87,''),(204,'MongoMart Alabaster',NULL,88,88,''),(205,'MongoMart Prattville',NULL,89,89,''),(206,'MongoMart Rivergate',NULL,90,90,''),(207,'MongoMart Chattanooga',NULL,91,91,''),(208,'MongoMart Meridian',NULL,92,92,''),(209,'MongoMart Gulfport',NULL,93,93,''),(210,'MongoMart Winchester Rd',NULL,94,94,''),(211,'MongoMart Elizabethtown',NULL,95,95,''),(212,'MongoMart CMH - Port Columbus International Airport',NULL,96,96,''),(213,'MongoMart CLE - Cleveland Hopkins International Airport',NULL,97,97,''),(214,'MongoMart Sandusky',NULL,98,98,''),(215,'MongoMart IND - Indianapolis International Airport',NULL,99,99,''),(216,'MongoMart Highland',NULL,100,100,''),(217,'MongoMart Valparaiso',NULL,101,101,''),(218,'MongoMart Port Huron',NULL,102,102,''),(219,'MongoMart - Briarwood Mall ',NULL,103,103,''),(220,'MongoMart Dearborn',NULL,104,104,''),(221,'MongoMart Battle Creek',NULL,105,105,''),(222,'MongoMart Benton Harbor',NULL,106,106,''),(223,'MongoMart Jackson',NULL,107,107,''),(224,'MongoMart Grand Rapids',NULL,108,108,''),(225,'MongoMart Grand Rapids',NULL,109,109,''),(226,'MongoMart Fox Point',NULL,110,110,''),(227,'MongoMart BTV - Burlington International Airport',NULL,111,111,''),(228,'MongoMart Stevens Point',NULL,112,112,''),(229,'MongoMart Appleton West',NULL,113,113,''),(230,'MongoMart Appleton East',NULL,114,114,''),(231,'MongoMart Fond Du Lac',NULL,115,115,''),(232,'MongoMart Lake Geneva',NULL,116,116,'');
/*!40000 ALTER TABLE `stores` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-05-22 15:52:27
