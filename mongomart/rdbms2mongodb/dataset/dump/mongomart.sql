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
USE mongomart;
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
-- Table structure for table `categories`
--

DROP TABLE IF EXISTS `categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `categories` (
  `name` varchar(45) NOT NULL,
  `num_items` int(11) DEFAULT '0',
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categories`
--

LOCK TABLES `categories` WRITE;
/*!40000 ALTER TABLE `categories` DISABLE KEYS */;
INSERT INTO `categories` VALUES ('Apparel',6),('Books',3),('Electronics',3),('Kitchen',3),('Office',2),('Stickers',2),('Swag',2),('Umbrellas',2);
/*!40000 ALTER TABLE `categories` ENABLE KEYS */;
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
-- Table structure for table `geo`
--

DROP TABLE IF EXISTS `geo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `geo` (
  `id` int(11) NOT NULL,
  `longitude` decimal(11,8) NOT NULL,
  `latitude` decimal(10,8) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `geo`
--

LOCK TABLES `geo` WRITE;
/*!40000 ALTER TABLE `geo` DISABLE KEYS */;
INSERT INTO `geo` VALUES (1,-71.71242500,42.52738200),(2,-71.83595200,42.20338400),(3,-71.39650700,42.30139200),(4,-71.02280000,42.21660000),(5,-70.99903100,42.21626700),(6,-70.29747000,41.66782400),(7,-71.35234800,41.93983500),(8,-71.43190800,42.95694400),(9,-72.32627100,43.62557600),(10,-70.33503000,43.63397600),(11,-70.23165900,44.11957900),(12,-72.80677800,41.55009800),(13,-72.80915800,41.55165500),(14,-72.99037900,41.27971600),(15,-73.22476700,41.23108900),(16,-74.21213500,40.88555500),(17,-74.22778300,40.14762100),(18,-74.35868800,40.80147600),(19,-74.95761900,39.94078800),(20,-87.94628700,42.24305300),(21,-88.11024500,41.93795000),(22,-88.72285700,41.94829600),(23,-88.21199700,41.76032200),(24,-87.85017400,41.17259600),(25,-73.02696800,41.24685100),(26,-75.04039400,39.43129800),(27,-74.39637800,40.45650500),(28,-73.98209400,40.76988200),(29,-74.36489800,41.45337600),(30,-73.90930900,40.75334500),(31,-73.72404900,40.66312000),(32,-73.43682700,40.67925200),(33,-72.69431300,40.92991300),(34,-73.85120300,42.68950400),(35,-73.98322100,41.96639900),(36,-73.91199700,41.61094000),(37,-76.17052800,43.06695300),(38,-74.37070500,41.45187400),(39,-75.95938900,43.97506000),(40,-78.73188700,42.93403800),(41,-77.63201900,43.07772400),(42,-80.04642500,40.34529100),(43,-79.80014800,40.43139600),(44,-80.09910000,42.07206000),(45,-76.83111600,41.24491100),(46,-75.67740900,40.25259520),(47,-75.54395300,39.82652700),(48,-77.00625400,38.89712100),(49,-76.92558500,38.61744700),(50,-76.86303700,39.08559000),(51,-76.73284100,38.94535100),(52,-77.14860300,39.02330100),(53,-76.86358100,39.21714700),(54,-77.77084300,39.62467500),(55,-77.13127900,38.85045200),(56,-77.16996800,38.77481800),(57,-78.16511000,39.16421000),(58,-76.08811000,36.77465000),(59,-77.39353900,37.25383400),(60,-81.12274200,35.26077700),(61,-78.96073300,35.07228500),(62,-84.28464500,34.05170800),(63,-84.68343400,34.03486600),(64,-84.75784300,33.72742100),(65,-84.44448600,33.64122900),(66,-84.36327400,33.82481000),(67,-83.85353900,34.29737100),(68,-83.42545600,33.94734400),(69,-82.08070600,33.46587000),(70,-81.55374900,30.18949700),(71,-85.64465300,30.18826700),(72,-86.42314100,30.38757300),(73,-81.30913800,28.43056500),(74,-81.30913800,28.43056500),(75,-81.30913800,28.43056500),(76,-81.30913800,28.43056500),(77,-80.65098100,28.08195700),(78,-80.45760500,27.64169800),(79,-80.18897700,25.79401800),(80,-80.14059000,26.06754700),(81,-80.31907100,26.15618900),(82,-80.25118500,26.09454100),(83,-80.20118000,26.66385000),(84,-80.13402700,26.36475600),(85,-82.50475300,27.95793300),(86,-81.64426000,28.24956000),(87,-80.27163100,27.24364200),(88,-86.80446600,33.22568900),(89,-86.39852000,32.45631000),(90,-86.68396000,36.30593100),(91,-85.14965100,35.03815100),(92,-88.66850000,32.36271000),(93,-89.09767900,30.44689000),(94,-89.80493900,35.04707700),(95,-85.89136500,37.73996400),(96,-82.88920800,39.99822000),(97,-82.90294400,40.21127300),(98,-82.67083000,41.41625200),(99,-86.29806400,39.71469500),(100,-87.46818000,41.52766000),(101,-87.02500200,41.46823500),(102,-82.45856500,43.04236200),(103,-83.74638300,42.24113200),(104,-83.20329300,42.32825500),(105,-85.17826800,42.26499200),(106,-86.42292800,42.07694200),(107,-84.42576600,42.26889000),(108,-85.76125300,42.87711300),(109,-85.58150500,42.91532900),(110,-87.91436800,43.17571600),(111,-73.15475800,44.46910800),(112,-89.51533500,44.52233500),(113,-88.47508200,44.27494800),(114,-88.35959600,44.24145100),(115,-88.48036200,43.78466400),(116,-88.41808000,42.60070000);
/*!40000 ALTER TABLE `geo` ENABLE KEYS */;
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
-- Table structure for table `items`
--

DROP TABLE IF EXISTS `items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `items` (
  `id` int(11) NOT NULL,
  `title` varchar(45) DEFAULT NULL,
  `description` text COMMENT '	',
  `price` decimal(10,0) DEFAULT NULL,
  `stars` int(11) DEFAULT NULL,
  `img_url` varchar(2083) DEFAULT NULL,
  `slogan` varchar(100) DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `items`
--

LOCK TABLES `items` WRITE;
/*!40000 ALTER TABLE `items` DISABLE KEYS */;
INSERT INTO `items` VALUES (1,'Gray Hooded Sweatshirt','Unless you live in a nudist colony, there are moments when the chill you feel demands that you put on something warm, and for those times, there\'s nothing better than this sharp MongoDB hoodie. Made of 100% cotton, this machine washable, mid-weight hoodie is all you need to stay comfortable when the temperature drops. And, since being able to keep your vital stuff with you is important, the hoodie features two roomy kangaroo pockets to ensure nothing you need ever gets lost.',30,0,'/img/products/hoodie.jpg','The top hooded sweatshirt we offer',NULL),(2,'Coffee Mug','A mug is a type of cup used for drinking hot beverages, such as coffee, tea, hot chocolate or soup. Mugs usually have handles, and hold a larger amount of fluid than other types of cup. Usually a mug holds approximately 12 US fluid ounces (350 ml) of liquid; double a tea cup. A mug is a less formal style of drink container and is not usually used in formal place settings, where a teacup or coffee cup is preferred.',13,0,'/img/products/mug.jpg','Keep your coffee hot!',NULL),(3,'Stress Ball','The moment life piles more onto your already heaping plate and you start feeling hopelessly overwhelmed, take a stress ball in hand and squeeze as hard as you can. Take a deep breath and just let that tension go. Repeat as needed. It will all be OK! Having something small, portable and close at hand is a must for stress management.',5,0,'/img/products/stress-ball.jpg','Squeeze your stress away',NULL),(4,'Track Jacket','Crafted from ultra-soft combed cotton, this essential jacket features sporty contrast tipping and MongoDB\'s signature embroidered leaf.',45,0,'/img/products/track-jacket.jpg','Go to the track in style!',NULL),(5,'Women\'s T-shirt','Crafted from ultra-soft combed cotton, this essential t-shirt features sporty contrast tipping and MongoDB\'s signature leaf.',45,0,'/img/products/white-mongo.jpg','MongoDB shirt in-style',NULL),(6,'Brown Carry-all Bag','Let your style speak for itself with this chic brown carry-all bag. Featuring a nylon exterior with solid contrast trim, brown in color, and MongoDB logo',5,0,'/img/products/brown-bag.jpg','Keep extra items here',NULL),(7,'Brown Tumbler','The MongoDB Insulated Travel Tumbler is smartly designed to maintain temperatures and go anywhere. Dual wall construction will keep your beverages hot or cold for hours and a slide lock lid helps minimize spills.',9,0,'/img/products/brown-tumbler.jpg','Bring your coffee to go',NULL),(8,'Pen (Green)','Erase and rewrite repeatedly without damaging documents. The needlepoint tip creates clear precise lines and the thermo-sensitive gel ink formula disappears with erasing friction.',2,0,'/img/products/green-pen.jpg','The only pen you\'ll ever need',NULL),(9,'Pen (Black)','Erase and rewrite repeatedly without damaging documents. The needlepoint tip creates clear precise lines and the thermo-sensitive gel ink formula disappears with erasing friction.',2,0,'/img/products/pen.jpg','The only pen you\'ll ever need',NULL),(10,'Green T-shirt','Crafted from ultra-soft combed cotton, this essential t-shirt features sporty contrast tipping and MongoDB\'s signature leaf.',20,0,'/img/products/green-tshirt.jpg','MongoDB community shirt',NULL),(11,'MongoDB The Definitive Guide','Manage the huMONGOus amount of data collected through your web application with MongoDB. This authoritative introduction—written by a core contributor to the project—shows you the many advantages of using document-oriented databases, and demonstrates how this reliable, high-performance system allows for almost infinite horizontal scalability.',20,0,'/img/products/guide-book.jpg','2nd Edition',NULL),(12,'Leaf Sticker','Waterproof vinyl, will last 18 months outdoors.  Ideal for smooth flat surfaces like laptops, journals, windows etc.  Easy to remove.  50% discounts on all orders of any 6+',1,0,'/img/products/leaf-sticker.jpg','Add to your sticker collection',NULL),(13,'USB Stick (Green)','MongoDB\'s Turbo USB 3.0 features lightning fast transfer speeds of up to 10X faster than standard MongoDB USB 2.0 drives. This ultra-fast USB allows for fast transfer of larger files such as movies and videos.',20,0,'/img/products/greenusb.jpg','1GB of space',NULL),(14,'USB Stick (Leaf)','MongoDB\'s Turbo USB 3.0 features lightning fast transfer speeds of up to 10X faster than standard MongoDB USB 2.0 drives. This ultra-fast USB allows for fast transfer of larger files such as movies and videos.',20,0,'/img/products/leaf-usb.jpg','1GB of space',NULL),(15,'Scaling MongoDB','Create a MongoDB cluster that will grow to meet the needs of your application. With this short and concise book, you\'ll get guidelines for setting up and using clusters to store a large volume of data, and learn how to access the data efficiently. In the process, you\'ll understand how to make your application work with a distributed database system.',29,0,'/img/products/scaling-book.jpg','2nd Edition',NULL),(16,'Powered by MongoDB Sticker','Waterproof vinyl, will last 18 months outdoors.  Ideal for smooth flat surfaces like laptops, journals, windows etc.  Easy to remove.  50% discounts on all orders of any 6+',1,0,'/img/products/sticker.jpg','Add to your sticker collection',NULL),(17,'MongoDB Umbrella (Brown)','Our crook handle stick umbrella opens automatically with the push of a button. A traditional umbrella with classic appeal.',21,0,'/img/products/umbrella-brown.jpg','Premium Umbrella',NULL),(18,'MongoDB Umbrella (Gray)','Our crook handle stick umbrella opens automatically with the push of a button. A traditional umbrella with classic appeal.',21,0,'/img/products/umbrella.jpg','Premium Umbrella',NULL),(19,'MongoDB University Book','Keep the MongoDB commands you\'ll need at your fingertips with this concise book.',4,0,'/img/products/univ-book.jpg','A concise summary of MongoDB commands',NULL),(20,'MongoDB University T-shirt','Crafted from ultra-soft combed cotton, this essential t-shirt features sporty contrast tipping and MongoDB\'s signature leaf.',45,0,'/img/products/univ-tshirt.jpg','Show Your MDBU Alumni Status',NULL),(21,'USB Stick','MongoDB\'s Turbo USB 3.0 features lightning fast transfer speeds of up to 10X faster than standard MongoDB USB 2.0 drives. This ultra-fast USB allows for fast transfer of larger files such as movies and videos.',40,0,'/img/products/leaf-usb.jpg','5GB of space',NULL),(22,'Water Bottle','High quality glass bottle provides a healthier way to drink.  Silicone sleeve provides a good grip, a see-through window, and protects the glass vessel.  Eliminates toxic leaching that plastic can cause.  Innovative design holds 22-1/2 ounces.  Dishwasher safe',23,0,'/img/products/water-bottle.jpg','Glass water bottle',NULL),(23,'WiredTiger T-shirt','Crafted from ultra-soft combed cotton, this essential t-shirt features sporty contrast tipping and MongoDB\'s signature leaf.',22,0,'/img/products/wt-shirt.jpg','Unleash the tiger',NULL);
/*!40000 ALTER TABLE `items` ENABLE KEYS */;
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
-- Table structure for table `reviews`
--

DROP TABLE IF EXISTS `reviews`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reviews` (
  `id` int(11) NOT NULL COMMENT '	',
  `name` varchar(45) DEFAULT NULL,
  `date` datetime DEFAULT NULL,
  `comment` text,
  `stars` int(11) DEFAULT NULL,
  `item_id` varchar(45) DEFAULT NULL,
  `items_id` int(11) NOT NULL,
  PRIMARY KEY (`id`,`items_id`),
  KEY `fk_reviews_items1_idx` (`items_id`),
  CONSTRAINT `fk_reviews_items1` FOREIGN KEY (`items_id`) REFERENCES `old_items` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reviews`
--

LOCK TABLES `reviews` WRITE;
/*!40000 ALTER TABLE `reviews` DISABLE KEYS */;
/*!40000 ALTER TABLE `reviews` ENABLE KEYS */;
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