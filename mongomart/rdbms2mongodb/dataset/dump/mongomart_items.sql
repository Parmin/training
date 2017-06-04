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
