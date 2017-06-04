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
-- Table structure for table `addresses`
--

DROP TABLE IF EXISTS `addresses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `addresses` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '	',
  `line1` varchar(100) DEFAULT NULL,
  `line2` varchar(45) DEFAULT NULL,
  `city` varchar(45) DEFAULT NULL COMMENT '	',
  `state` char(2) DEFAULT NULL COMMENT '			',
  `zip` varchar(5) DEFAULT NULL,
  `country` varchar(2) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=117 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `addresses`
--

LOCK TABLES `addresses` WRITE;
/*!40000 ALTER TABLE `addresses` DISABLE KEYS */;
INSERT INTO `addresses` VALUES (1,'1790 Biscayne Blvd','Ste D','Miami','FL','33132','US'),(2,'385 Southbridge Street','S080','Auburn','MA','01501','US'),(3,'3450 Wrightsboro Rd.','Ste. 1075','Augusta ','GA','30909','US'),(4,'442 Briarwood Circle ','Ste. F125','Ann Arbor','MI','48108','US'),(5,'237 Cross Creek Mall','#TC-7','Fayetteville','NC','28303','US'),(6,'1 Crossgates Mall Road','#L101A','Albany','NY','12203','US'),(7,'3849 S Delsea Dr','Ste F18A','Vineland','NJ','08360','US'),(8,'9090 Destiny USA Drive','#E106','Syracuse','NY','13204','US'),(9,'1208 Fox Valley Center Drive','#H5','Aurora','IL','60504','US'),(10,'1 N Galleria Dr','#D101','Middletown','NY','10941','US'),(11,'3700 Atlanta Highway','#100','Athens','GA','30606','US'),(12,'2034 Green Acres Mall','#223B','Valley Stream','NY','11581','US'),(13,'122 Hawthorn Center','#526','Vernon Hills','IL','60061','US'),(14,'1300 Ulster Avenue','#L03','Kingston','NY','12401','US'),(15,'6200 20th St','Ste 618','Vero Beach','FL','32966','US'),(16,'1700 W New Haven Ave','Ste 827','Melbourne','FL','32904','US'),(17,'470 Lewis Avenue','#23','Meriden','CT','06451','US'),(18,'275 Millcreek Mall','','Erie','PA','16565','US'),(19,'2001 South Rd #209','','Poughkeepsie','NY','12601','US'),(20,'12801 W Sunrise Blvd','#283','Sunrise','FL','33323','US'),(21,'250 Granite Street','#1098','Braintree','MA','02184','US'),(22,'230 Southpark Circle','#F70','Colonial Heights','VA','23834','US'),(23,'11110 Mall Circle','','Waldorf','MD','20603','US'),(24,'One Sunrise Mall','#2090','Massapequa','NY','11758','US'),(25,'10300 Little Patuxent Pkwy','#2385','Columbia','MD','21044','US'),(26,'6000 Glades Road','#1097','Boca Raton','FL','33431','US'),(27,'3222 NW Federal Hwy','','Jensen Beach','FL','34957','US'),(28,'5065 Main Street','Suite 133','Trumbull','CT','06611','US'),(29,'17301 Valley Mall Road','#538','Hagerstown','MD','21740','US'),(30,'7101 Democracy Blvd','','Bethesda','MD','20817','US'),(31,'6000 N. Terminal Pkwy','','Atlanta','GA','30320','US'),(32,'3335 Cobb Pkwy Nw','','Acworth','GA','30101','US'),(33,'100 S Colonial Dr','','Alabaster','AL','35007','US'),(34,'975 N Point Dr','','Alpharetta','GA','30022','US'),(35,'2411 S Kensington Dr','','Appleton','WI','54915','US'),(36,'4240 W Wisconsin Ave','','Appleton','WI','54913','US'),(37,'1337 S Washington St','','North Attleboro','MA','02760','US'),(38,'649 Turner St','','Auburn','ME','04210','US'),(39,'1200 Airport Drive','','S. Burlington','VT','5403','US'),(40,'4200 Genesee Street','','Cheektowaga','NY','14225','US'),(41,'5799 Leesburg Pike','','Falls Church','VA','22041','US'),(42,'12765 Harper Village Dr ','Ste 160','Battle Creek','MI','49014','US'),(43,'1515 Orchard Xing','','Benton Harbor','MI','49022','US'),(44,'350 W Army Trail Rd','','Bloomingdale','IL','60108','US'),(45,'15800 Collington Rd','','Bowie','MD','20715','US'),(46,'550 Grossman Dr','','Braintree','MA','02184','US'),(47,'2537 Piedmont Rd NE','','Atlanta','GA','30324','US'),(48,'143 Airport Blvd','','Cleveland','OH','44181','US'),(49,'4600 International Gateway','','Columbus','OH','43219','US'),(50,'793 Iyannough Rd ','Ste A','Hyannis','MA','02601','US'),(51,'2290 Gunbarrel Rd','Ste 114','Chattanooga','TN','37421','US'),(52,'4807 Concord Pike','','Wilmington','DE','19803','US'),(53,'I-95 Southbound past exit 40','','Milford','CT','6460','US'),(54,'6300 Grandview Pkwy','','Davenport','FL','33837','US'),(55,'2200 S University Dr','','Davie','FL','33324','US'),(56,'16221 Ford Rd Fairlane Meadows','','Dearborn','MI','48126','US'),(57,'34940 Emerald Coast Pkwy','Unit 150','Destin','FL','32541','US'),(58,'6875 Douglas Blvd','','Douglasville','GA','30135','US'),(59,'300 State Route 18 ','Suite 4','East Brunswick','NJ','08816','US'),(60,'410 State Route 10','','East Hanover','NJ','07936','US'),(61,'2050 N Dixie Hwy','','Elizabethtown','KY','42701','US'),(62,'100 Aviation Blvd.','','Ft. Lauderdale','FL','33315','US'),(63,'335 N Pioneer Rd','','Fond Du Lac','WI','54935','US'),(64,'8755 N. Port Washington Rd.','','Fox Point','WI','53217','US'),(65,'1 Worcester Rd','','Framingham','MA','01701','US'),(66,'670 Dawsonville Hwy','','Gainesville','GA','30501','US'),(67,'3054 E Franklin Blvd','','Gastonia','NC','28056','US'),(68,'4830 Wilson Ave SW','','Grandville','MI','49418','US'),(69,'2650 E Beltline Ave SE','','Grand Rapids','MI','49546','US'),(70,'10545 Hwy 49','','Gulfport','MS','39503','US'),(71,'2345 Marketplace Dr','','Rochester','NY','14623','US'),(72,'10243 Indianapolis Blvd','','Highland','IN','46322','US'),(73,'4250 Route 9','','Howell','NJ','07731','US'),(74,'7800 Col. H. Weir Cook Memorial Dr.','','Indianapolis','IN','46241','US'),(75,'2700 Crego Rd; I-88, West of the Peace Road exit Mile post 93','','DeKalb','IL','60115','US'),(76,'1014 Jackson Xing','','Jackson','MI','49202','US'),(77,'1584 N State Route 50','','Bourbonnais','IL','60914','US'),(78,'700 N Edwards Blvd','','Lake Geneva','WI','53147','US'),(79,'14160 Baltimore Ave','Laurel Lakes Centre','Laurel','MD','20707','US'),(80,'274 Plainfield Rd','','West Lebanon','NH','03784','US'),(81,'33 Orchard Hill Park Dr','','Leominster','MA','01453','US'),(82,'5001 Northern Blvd','','Long Island City','NY','11101','US'),(83,'One Airport Blvd.','','Orlando','FL','32827','US'),(84,'One Airport Blvd.','','Orlando','FL','32827','US'),(85,'One Airport Blvd.','','Orlando','FL','32827','US'),(86,'One Airport Blvd.','','Orlando','FL','32827','US'),(87,'1500 S Willow St','','Manchester','NH','03103','US'),(88,'470 Lewis Ave','','Meriden','CT','06450','US'),(89,'133 S Frontage Rd','','Meridian','MS','39301','US'),(90,'1100 N Galleria Dr','','Middletown','NY','10941','US'),(91,'200 Mall Circle Dr','','Monroeville','PA','15146','US'),(92,'1420 Nixon Dr ','Eastgate Square','Mt Laurel','NJ','08054','US'),(93,'115 Lycoming Mall Cir','','Muncy','PA','17756','US'),(94,'53 Boston Post Rd','','Orange','CT','06477','US'),(95,'1000 E 23rd St','','Panama City','FL','32405','US'),(96,'4611 24th Ave ','Ft Gratiot Center','Ft Gratiot','MI','48059','US'),(97,'364 Maine Mall Rd','Box #301','South Portland','ME','04106','US'),(98,'Upland Square Drive ','Suite 200','Stowe','PA','19464','US'),(99,'2431 Cobbs Ford Rd','','Prattville','AL','36066','US'),(100,'3334 Princess Anne Rd','','Virginia Beach','VA','23456','US'),(101,'2311 Gallatin Pike N','','Madison','TN','37115','US'),(102,'1440 Old Country Rd','Suite 100','Riverhead','NY','11901','US'),(103,'4210 Milan Rd','','Sandusky','OH','44870','US'),(104,'5000 Alicia Dr','','Bethel Park','PA','15102','US'),(105,'1725 N Dale Mabry Hwy','','Tampa','FL','33607','US'),(106,'6555 Frontier Dr','','Springfield','VA','22150','US'),(107,'1145 Commons Cir','','Plover','WI','54467','US'),(108,'9930 Southside Blvd','','Jacksonville','FL','32256','US'),(109,'50 Massachusetts Avenue NE','','Washington','DC','20002','US'),(110,'1880 Broadway','','New York','NY','10023','US'),(111,'91 Silhavy Rd ','Ste 101','Valparaiso','IN','46383','US'),(112,'21085 Salmon Run Mall Loop W','','Watertown','NY','13601','US'),(113,'1040 S State Road 7','','Wellington','FL','33414','US'),(114,'30 Andrews Dr','','Woodland Park','NJ','07424','US'),(115,'601 East Jubal Early Dr','','Winchester','VA','22601','US'),(116,'7771 Winchester Rd','','Memphis','TN','38125','US');
/*!40000 ALTER TABLE `addresses` ENABLE KEYS */;
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
