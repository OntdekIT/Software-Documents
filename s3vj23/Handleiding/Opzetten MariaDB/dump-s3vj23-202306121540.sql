-- MySQL dump 10.13  Distrib 8.0.19, for Win64 (x86_64)
--
-- Host: localhost    Database: s3vj23
-- ------------------------------------------------------
-- Server version	5.5.5-10.11.2-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `hibernate_sequence`
--

DROP TABLE IF EXISTS `hibernate_sequence`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hibernate_sequence` (
  `next_not_cached_value` bigint(21) NOT NULL,
  `minimum_value` bigint(21) NOT NULL,
  `maximum_value` bigint(21) NOT NULL,
  `start_value` bigint(21) NOT NULL COMMENT 'start value when sequences is created or value if RESTART is used',
  `increment` bigint(21) NOT NULL COMMENT 'increment value',
  `cache_size` bigint(21) unsigned NOT NULL,
  `cycle_option` tinyint(1) unsigned NOT NULL COMMENT '0 if no cycles are allowed, 1 if the sequence should begin a new cycle when maximum_value is passed',
  `cycle_count` bigint(21) NOT NULL COMMENT 'How many cycles have been done'
) ENGINE=InnoDB SEQUENCE=1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hibernate_sequence`
--

LOCK TABLES `hibernate_sequence` WRITE;
/*!40000 ALTER TABLE `hibernate_sequence` DISABLE KEYS */;
INSERT INTO `hibernate_sequence` VALUES (1,1,9223372036854775806,1,1,1000,0,0);
/*!40000 ALTER TABLE `hibernate_sequence` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `location`
--

DROP TABLE IF EXISTS `location`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `location` (
  `locationid` bigint(20) NOT NULL AUTO_INCREMENT,
  `direction` varchar(255) DEFAULT NULL,
  `height` float NOT NULL,
  `is_outside` bit(1) NOT NULL,
  `latitude` float NOT NULL,
  `longitude` float NOT NULL,
  PRIMARY KEY (`locationid`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `location`
--

LOCK TABLES `location` WRITE;
/*!40000 ALTER TABLE `location` DISABLE KEYS */;
INSERT INTO `location` VALUES (7,'E',10,_binary '\0',51.5474,5.04709),(8,'E',10,_binary '\0',51.5612,5.06723),(10,'E',10,_binary '\0',51.5403,5.08047),(12,'S',50,_binary '',51.577,5.09702),(13,'E',10,_binary '',51.5589,5.0665),(14,'N',10,_binary '',51.5599,5.07736),(15,'N',10,_binary '',51.557,5.10663),(16,'S',10,_binary '',51.549,5.05069),(17,'S',10,_binary '',51.5405,5.06897),(18,'W',10,_binary '',51.5843,5.0162),(19,'E',10,_binary '',51.5823,5.00256),(20,'W',10,_binary '',51.5781,4.99295),(21,'S',10,_binary '',51.587,4.97537),(22,'S',10,_binary '',51.5714,4.98474),(23,'N',10,_binary '',51.5795,5.07733),(24,'N',10,_binary '',51.5802,5.08682),(25,'N',10,_binary '',51.5821,5.10071),(26,'E',10,_binary '',51.6121,5.14792),(27,'S',10,_binary '',51.577,5.13892);
/*!40000 ALTER TABLE `location` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mail`
--

DROP TABLE IF EXISTS `mail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mail` (
  `mail_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `body` varchar(255) DEFAULT NULL,
  `footer` varchar(255) DEFAULT NULL,
  `header` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`mail_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mail`
--

LOCK TABLES `mail` WRITE;
/*!40000 ALTER TABLE `mail` DISABLE KEYS */;
/*!40000 ALTER TABLE `mail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `region`
--

DROP TABLE IF EXISTS `region`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `region` (
  `id` bigint(20) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `region`
--

LOCK TABLES `region` WRITE;
/*!40000 ALTER TABLE `region` DISABLE KEYS */;
INSERT INTO `region` VALUES (1,'Tilburg Noord'),(2,'Tilburg Oud-Noord'),(3,'Tilburg West'),(4,'Tilburg Reeshof'),(5,'Tilburg Centrum'),(6,'Tilburg Zuid'),(7,'Trouwlaan'),(8,'Moerenburg'),(9,'Het Zand'),(10,'Industrieterrein-oost'),(11,'Groenewoud'),(12,'Tuindorp De Kievit'),(13,'Armhoef'),(14,'De Lijnse Hoek'),(15,'Korvel'),(16,'Zorgvlied'),(17,'Jeruzalem'),(18,'De Blaak'),(19,'Hoefstraat'),(20,'Koolhoven'),(21,'Witbrant'),(22,'Groeseind'),(23,'Stokhasselt-zuid'),(24,'Rooi Harten'),(25,'De Oude Warande'),(26,'Wandelbos-zuid'),(27,'Koningshoeven'),(28,'Hasselt'),(29,'Mariaziekenhuis-Vredeburcht'),(30,'Heikant'),(31,'Dalem'),(32,'Het Laar'),(33,'Vlashof'),(34,'Wandelbos-noord'),(35,'Stokhasselt-noord'),(36,'Huibeven'),(37,'Heerevelden'),(38,'Industrieterrein Loven'),(39,'Campenhoef'),(40,'Loven'),(41,'Dongewijk'),(42,'Gesworen Hoek'),(43,'Industriestrook Goirke-Kanaaldijk'),(44,'Heyhoef'),(45,'De Quirijnstok'),(46,'Industriestrook Lovense-Kanaaldijk'),(47,'Bouwmeester'),(48,'Noordhoek'),(49,'Binnenstad'),(50,'Fatima');
/*!40000 ALTER TABLE `region` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `region_cords`
--

DROP TABLE IF EXISTS `region_cords`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `region_cords` (
  `id` bigint(20) NOT NULL,
  `x_cord` double NOT NULL,
  `y_cord` double NOT NULL,
  `region_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FKiu776j92u2nvrsrdikg2stjvi` (`region_id`),
  CONSTRAINT `FKiu776j92u2nvrsrdikg2stjvi` FOREIGN KEY (`region_id`) REFERENCES `region` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `region_cords`
--

LOCK TABLES `region_cords` WRITE;
/*!40000 ALTER TABLE `region_cords` DISABLE KEYS */;
INSERT INTO `region_cords` VALUES (6,51.560042,5.091805,2),(7,51.561754,5.093154,2),(8,51.561874,5.091833,2),(9,51.56751,5.088281,2),(10,51.567176,5.08181,2),(11,51.561027,5.08002,2),(12,51.543646,5.083237,3),(13,51.543826,5.093056,3),(14,51.548777,5.104097,3),(15,51.552553,5.100244,3),(16,51.551239,5.095844,3),(17,51.551692,5.09549,3),(18,51.551199,5.088973,3),(19,51.549257,5.088222,3),(20,51.54779,5.085087,3),(21,51.568134,5.075008,4),(22,51.567214,5.076759,4),(23,51.566974,5.079464,4),(24,51.566994,5.081139,4),(25,51.567601,5.083669,4),(26,51.567787,5.087083,4),(27,51.572955,5.084623,4),(28,51.576863,5.084248,4),(29,51.576569,5.07736,4),(30,51.571602,5.079183,4),(31,51.569988,5.0765,4),(32,51.558593,5.03868,5),(33,51.557992,5.041299,5),(34,51.556227,5.063909,5),(35,51.562992,5.065267,5),(36,51.56636,5.042596,5),(37,51.551159,5.088699,6),(38,51.551652,5.095546,6),(39,51.551265,5.095932,6),(40,51.555268,5.106349,6),(41,51.561238,5.103719,6),(42,51.559981,5.096958,6),(43,51.559997,5.091738,6),(44,51.557203,5.09305,6),(45,51.552596,5.090554,6),(47,51.54403,5.07753,7),(48,51.543643,5.08337,7),(49,51.547863,5.085072,7),(50,51.549244,5.08819,7),(51,51.551149,5.08872,7),(52,51.552373,5.088312,7),(53,51.551205,5.084637,7),(54,51.550825,5.078157,7),(55,51.549024,5.076838,7),(56,51.562105,5.109362,8),(57,51.545414,5.119246,8),(58,51.547149,5.119955,8),(59,51.550565,5.124869,8),(60,51.554408,5.121734,8),(61,51.557356,5.124075,8),(62,51.559584,5.128562,8),(63,51.561486,5.127188,8),(64,51.566635,5.127167,8),(65,51.566414,5.042479,9),(66,51.563599,5.061804,9),(67,51.568648,5.062575,9),(68,51.572089,5.061513,9),(69,51.575569,5.063059,9),(70,51.577263,5.047937,9),(71,51.57681,5.046724,9),(72,51.574229,5.09682,10),(73,51.570822,5.10091,10),(74,51.570115,5.114558,10),(75,51.570662,5.115138,10),(76,51.570008,5.117779,10),(77,51.57731,5.12402,10),(78,51.583383,5.110961,10),(79,51.583943,5.108631,10),(80,51.581097,5.106248,10),(81,51.580577,5.104154,10),(82,51.579416,5.102866,10),(83,51.576769,5.104391,10),(84,51.574009,5.100522,10),(85,51.536926,5.076172,11),(86,51.535345,5.094364,11),(87,51.531439,5.100137,11),(88,51.536598,5.108077,11),(89,51.540869,5.113508,11),(90,51.542711,5.113401,11),(91,51.545106,5.111769,11),(92,51.551631,5.110019,11),(93,51.543885,5.093016,11),(94,51.543605,5.083411,11),(95,51.544012,5.077488,11),(96,51.583977,4.985841,12),(97,51.582597,4.99638,12),(98,51.585917,4.997504,12),(99,51.58441,5.00715,12),(100,51.585917,5.009339,12),(101,51.58815,5.005409,12),(102,51.591109,5.005992,12),(103,51.612307,4.949632,12),(104,51.611448,4.948795,12),(105,51.603059,4.967818,12),(106,51.601819,4.968806,12),(107,51.598061,4.967582,12),(108,51.597208,4.975675,12),(109,51.596235,4.977636,12),(110,51.594022,4.977936,12),(111,51.561218,5.103763,13),(112,51.555248,5.106274,13),(113,51.557116,5.11166,13),(114,51.562285,5.108731,13),(115,51.578003,5.073643,14),(116,51.57901,5.083002,14),(117,51.57877,5.088914,14),(118,51.578203,5.090933,14),(119,51.58123,5.093807,14),(120,51.581637,5.082314,14),(121,51.58279,5.076392,14),(122,51.545554,5.054078,15),(123,51.544433,5.0547,15),(124,51.54396,5.056236,15),(125,51.544046,5.077574,15),(126,51.549024,5.076855,15),(127,51.550718,5.078176,15),(128,51.553093,5.079184,15),(129,51.555088,5.077746,15),(130,51.553667,5.072059,15),(131,51.553147,5.064694,15),(132,51.554701,5.063664,15),(133,51.550518,5.060794,15),(134,51.547276,5.0569,15),(135,51.558026,5.04131,16),(136,51.547288,5.056807,16),(137,51.550597,5.060732,16),(138,51.550597,5.060732,16),(139,51.55468,5.063565,16),(140,51.55489,5.106476,17),(141,51.551731,5.110063,17),(142,51.552812,5.114336,17),(143,51.555867,5.112553,17),(144,51.556614,5.111415,17),(145,51.540207,5.033542,18),(146,51.539673,5.048229,18),(147,51.542129,5.04956,18),(148,51.5472,5.056903,18),(149,51.55798,5.041358,18),(150,51.558461,5.039597,18),(151,51.553626,5.037923,18),(152,51.553626,5.036527,18),(153,51.54973,5.036935,18),(154,51.546191,5.036085,18),(155,51.544379,5.029532,18),(156,51.567813,5.087091,19),(157,51.567224,5.090117,19),(158,51.567425,5.094465,19),(159,51.567565,5.095185,19),(160,51.568432,5.096671,19),(161,51.568478,5.098206,19),(162,51.568892,5.098195,19),(163,51.575533,5.090148,19),(164,51.57446,5.086069,19),(165,51.573593,5.086004,19),(166,51.572946,5.084544,19),(167,51.569481,4.967838,20),(168,51.564993,4.993264,20),(169,51.573769,4.993396,20),(170,51.577283,4.970465,20),(171,51.577343,4.969262,20),(172,51.573629,4.967012,20),(173,51.571308,4.96892,20),(174,51.565066,4.993174,21),(175,51.561518,5.018382,21),(176,51.569948,5.018038,21),(177,51.573762,4.993417,21),(178,51.573039,5.084627,22),(179,51.573466,5.085835,22),(180,51.574516,5.086173,22),(181,51.575606,5.089981,22),(182,51.576866,5.084213,22),(183,51.57885,5.066488,23),(184,51.578096,5.073415,23),(185,51.58283,5.076271,23),(186,51.583843,5.06798,23),(187,51.553087,5.064632,24),(188,51.553774,5.072124,24),(189,51.554995,5.07764,24),(190,51.555301,5.07779,24),(191,51.556282,5.064034,24),(192,51.554788,5.06354,24),(193,51.561571,5.01827,25),(194,51.558717,5.038783,25),(195,51.5664,5.04262,25),(196,51.570081,5.017966,25),(197,51.570135,5.018057,26),(198,51.56644,5.042473,26),(199,51.572495,5.04511,26),(200,51.575036,5.037457,26),(201,51.576349,5.029238,26),(202,51.57875,5.022781,26),(203,51.542679,5.113674,27),(204,51.545748,5.118226,27),(205,51.552746,5.114342,27),(206,51.551686,5.109911,27),(207,51.545414,5.111499,27),(208,51.569004,5.065873,28),(209,51.568691,5.066163,28),(210,51.567914,5.06987,28),(211,51.568097,5.072286,28),(212,51.568578,5.073381,28),(213,51.568574,5.074194,28),(214,51.568204,5.074929,28),(215,51.569948,5.076409,28),(216,51.571635,5.079118,28),(217,51.576533,5.07746,28),(218,51.575553,5.066517,28),(219,51.563592,5.06189,29),(220,51.563039,5.065325,29),(221,51.568608,5.066331,29),(222,51.568901,5.065901,29),(223,51.578503,5.066416,29),(224,51.580803,5.045192,29),(225,51.577276,5.048113,29),(226,51.575576,5.063068,29),(227,51.572129,5.061491,29),(228,51.568748,5.06264,29),(229,51.578103,5.073443,30),(230,51.579023,5.082869,30),(231,51.579143,5.085951,30),(232,51.57873,5.089032,30),(233,51.57819,5.090932,30),(234,51.581203,5.093862,30),(235,51.590596,5.096178,30),(236,51.594109,5.081838,30),(237,51.592676,5.082214,30),(238,51.587223,5.079796,30),(239,51.582817,5.07633,30),(240,51.577246,4.970286,31),(241,51.574925,4.986862,31),(242,51.580931,4.987328,31),(243,51.588411,4.984471,31),(244,51.59381,4.978094,31),(245,51.596129,4.977643,31),(246,51.597196,4.975711,31),(247,51.597329,4.972946,31),(248,51.592104,4.973483,31),(249,51.53952,5.048103,32),(250,51.536857,5.076223,32),(251,51.544017,5.077542,32),(252,51.54395,5.056516,32),(253,51.544591,5.054509,32),(254,51.545672,5.053875,32),(255,51.542276,5.049163,32),(256,51.574229,5.09695,45),(257,51.574009,5.10045,45),(258,51.57713,5.104387,45),(259,51.57929,5.102927,45),(260,51.581083,5.106233,45),(261,51.583803,5.108552,45),(262,51.58335,5.110925,45),(263,51.590749,5.096413,45),(264,51.581103,5.093764,45),(265,51.578216,5.0909,45),(266,51.577756,5.091028,45),(267,51.582777,5.076349,33),(268,51.58159,5.082305,33),(269,51.587523,5.084923,33),(270,51.588276,5.086469,33),(271,51.587883,5.089014,33),(272,51.592049,5.090171,33),(273,51.594109,5.081811,33),(274,51.592622,5.082134,33),(275,51.587216,5.079773,33),(276,51.57883,5.022727,34),(277,51.576269,5.029168,34),(278,51.575009,5.037397,34),(279,51.572482,5.045057,34),(280,51.576743,5.04689,34),(281,51.57727,5.048028,34),(282,51.58085,5.044936,34),(283,51.58293,5.028005,34),(284,51.58387,5.067962,35),(285,51.58281,5.076385,35),(286,51.587576,5.079978,35),(287,51.592802,5.08222,35),(288,51.594069,5.081855,35),(289,51.596341,5.071626,35),(290,51.591416,5.070508,35),(291,51.572149,5.005452,36),(292,51.570095,5.01797,36),(293,51.578776,5.022796,36),(294,51.580597,5.017094,36),(295,51.583617,5.01163,36),(296,51.584423,5.007131,36),(297,51.579276,5.005272,36),(298,51.576763,5.007129,36),(299,51.58017,4.995583,37),(300,51.578143,5.002161,37),(301,51.579236,5.005146,37),(302,51.584463,5.007087,37),(303,51.585903,4.997417,37),(304,51.562399,5.10912,38),(305,51.562919,5.111632,38),(306,51.570028,5.117786,38),(307,51.570675,5.115145,38),(308,51.570181,5.114715,38),(309,51.570822,5.100909,38),(310,51.565853,5.10681,38),(311,51.573749,4.993533,39),(312,51.572129,5.005436,39),(313,51.576749,5.007107,39),(314,51.577263,5.005069,39),(315,51.576743,5.002546,39),(316,51.57813,5.002235,39),(317,51.580077,4.995529,39),(318,51.560031,5.09204,40),(319,51.560077,5.096914,40),(320,51.561305,5.103678,40),(321,51.568448,5.098271,40),(322,51.568381,5.09666,40),(323,51.567534,5.09505,40),(324,51.567441,5.094449,40),(326,51.574809,4.986881,41),(327,51.573829,4.993423,41),(328,51.582497,4.996515,41),(329,51.58395,4.985801,41),(330,51.58111,4.98739,41),(331,51.57877,5.022783,42),(332,51.58287,5.027837,42),(333,51.591103,5.006005,42),(334,51.588063,5.005401,42),(335,51.585883,5.009296,42),(336,51.584503,5.007128,42),(337,51.58357,5.01154,42),(338,51.580717,5.016572,42),(339,51.575576,5.066334,43),(340,51.576803,5.084171,43),(341,51.575523,5.090173,43),(342,51.575763,5.091891,43),(343,51.577523,5.090066,43),(344,51.577923,5.09041,43),(345,51.57867,5.087425,43),(346,51.578616,5.082551,43),(347,51.577736,5.074864,43),(348,51.578496,5.066297,43),(349,51.576753,5.002546,44),(350,51.57729,5.005081,44),(351,51.576823,5.007153,44),(352,51.57927,5.005186,44),(353,51.578276,5.002244,44),(354,51.561278,5.1038,46),(355,51.562292,5.108631,46),(356,51.565306,5.10661,46),(357,51.570268,5.100514,46),(358,51.576603,5.093152,46),(359,51.577856,5.090554,46),(360,51.57723,5.089845,46),(361,51.575869,5.091993,46),(362,51.575483,5.090253,46),(363,51.572469,5.094227,46),(364,51.568348,5.098736,46),(365,51.567209,5.090116,40),(366,51.567496,5.08835,40),(367,51.561894,5.091869,40),(368,51.561747,5.093159,40),(369,51.563058,5.065315,47),(370,51.560983,5.080015,47),(371,51.567164,5.081833,47),(372,51.566984,5.081033,47),(373,51.56697,5.07945,47),(374,51.567224,5.076741,47),(375,51.568144,5.074971,47),(376,51.568548,5.074182,47),(377,51.568568,5.073341,47),(378,51.568101,5.072338,47),(379,51.567911,5.069858,47),(380,51.568601,5.066372,47),(381,51.556242,5.063942,48),(382,51.555298,5.07783,48),(383,51.561165,5.078619,48),(384,51.563046,5.065309,48),(385,51.550815,5.07825,49),(386,51.551205,5.084617,49),(387,51.552356,5.088275,49),(388,51.5526,5.090567,49),(389,51.557206,5.093051,49),(390,51.559981,5.09174,49),(391,51.561128,5.078738,49),(392,51.555095,5.07775,49),(393,51.553103,5.079236,49),(394,51.556189,5.063961,16),(395,51.54893,5.104022,50),(396,51.551732,5.110137,50),(397,51.554861,5.106464,50),(398,51.552553,5.100233,50);
/*!40000 ALTER TABLE `region_cords` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sensor`
--

DROP TABLE IF EXISTS `sensor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sensor` (
  `sensorid` bigint(20) NOT NULL AUTO_INCREMENT,
  `active_data` bit(1) NOT NULL,
  `sensor_data` int(11) NOT NULL,
  `sensor_typeid` bigint(20) DEFAULT NULL,
  `stationid` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`sensorid`),
  KEY `FKokblxlilng14k37vbnax547yi` (`sensor_typeid`),
  KEY `FK73l0iai9750tbfx3p3i1jtty6` (`stationid`),
  CONSTRAINT `FK73l0iai9750tbfx3p3i1jtty6` FOREIGN KEY (`stationid`) REFERENCES `station` (`stationid`),
  CONSTRAINT `FKokblxlilng14k37vbnax547yi` FOREIGN KEY (`sensor_typeid`) REFERENCES `sensor_type` (`typeid`)
) ENGINE=InnoDB AUTO_INCREMENT=106 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sensor`
--

LOCK TABLES `sensor` WRITE;
/*!40000 ALTER TABLE `sensor` DISABLE KEYS */;
INSERT INTO `sensor` VALUES (30,_binary '\0',5,4,11),(46,_binary '\0',25,1,12),(47,_binary '\0',55,5,12),(48,_binary '\0',3,7,12),(49,_binary '\0',26,1,11),(50,_binary '\0',51,5,11),(51,_binary '\0',3,7,11),(52,_binary '\0',25,1,10),(53,_binary '\0',51,5,10),(54,_binary '\0',3,7,10),(64,_binary '\0',25,1,12),(65,_binary '\0',55,5,12),(66,_binary '\0',3,7,12),(67,_binary '\0',26,1,11),(68,_binary '\0',51,5,11),(69,_binary '\0',3,7,11),(70,_binary '',30,1,20),(71,_binary '',33,5,20),(72,_binary '',3,7,20),(73,_binary '',31,1,17),(74,_binary '',39,5,17),(75,_binary '',3,7,17),(76,_binary '',31,1,11),(77,_binary '',40,5,11),(78,_binary '',3,7,11),(79,_binary '',29,1,18),(80,_binary '',43,5,18),(81,_binary '',3,7,18),(82,_binary '',29,1,25),(83,_binary '',39,5,25),(84,_binary '',3,7,25),(85,_binary '',30,1,29),(86,_binary '',36,5,29),(87,_binary '',3,7,29),(88,_binary '',41,1,15),(89,_binary '',24,5,15),(90,_binary '',3,7,15),(91,_binary '',30,1,12),(92,_binary '',42,5,12),(93,_binary '',3,7,12),(94,_binary '',27,1,16),(95,_binary '',34,5,16),(96,_binary '',3,7,16),(97,_binary '',30,1,26),(98,_binary '',40,5,26),(99,_binary '',3,7,26),(100,_binary '',30,1,27),(101,_binary '',50,5,27),(102,_binary '',3,7,27),(103,_binary '',30,1,28),(104,_binary '',42,5,28),(105,_binary '',3,7,28);
/*!40000 ALTER TABLE `sensor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sensor_type`
--

DROP TABLE IF EXISTS `sensor_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sensor_type` (
  `typeid` bigint(20) NOT NULL AUTO_INCREMENT,
  `type_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`typeid`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sensor_type`
--

LOCK TABLES `sensor_type` WRITE;
/*!40000 ALTER TABLE `sensor_type` DISABLE KEYS */;
INSERT INTO `sensor_type` VALUES (1,'Temperatuur'),(2,'Stikstof'),(3,'Koolstofdioxide'),(4,'Fijnstof'),(5,'Luchtvochtigheid'),(6,'Windsnelheid'),(7,'Batterij');
/*!40000 ALTER TABLE `sensor_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `station`
--

DROP TABLE IF EXISTS `station`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `station` (
  `stationid` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `database_tag` varchar(255) DEFAULT NULL,
  `is_public` bit(1) NOT NULL,
  `registration_code` bigint(20) NOT NULL,
  `location_locationid` bigint(20) DEFAULT NULL,
  `userid` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`stationid`),
  KEY `FKguexbm09vbcok067wdao85dw0` (`location_locationid`),
  KEY `FKjpfw49q2hwosivlesvqxjy6qo` (`userid`),
  CONSTRAINT `FKguexbm09vbcok067wdao85dw0` FOREIGN KEY (`location_locationid`) REFERENCES `location` (`locationid`),
  CONSTRAINT `FKjpfw49q2hwosivlesvqxjy6qo` FOREIGN KEY (`userid`) REFERENCES `user` (`userid`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `station`
--

LOCK TABLES `station` WRITE;
/*!40000 ALTER TABLE `station` DISABLE KEYS */;
INSERT INTO `station` VALUES (10,'Fontys Campus','MJS',_binary '',378,10,1),(11,'Blaak','MJS',_binary '',580,7,1),(12,'Spoorpark','MJS',_binary '',674,8,1),(14,'Meetstation','MJS',_binary '',402,12,1),(15,'Iepenpad','MJS',_binary '',562,13,1),(16,'Noordhoek','MJS',_binary '',980,14,1),(17,'Oisterwijksebaan','MJS',_binary '',687,15,1),(18,'Berkelvijver','MJS',_binary '',563,16,1),(19,'Ateletiekbaan','MJS',_binary '',604,17,1),(20,'Borselestraat','MJS',_binary '',964,18,1),(21,'Heerenveld','MJS',_binary '',939,19,1),(22,'Dongewijk','MJS',_binary '',972,20,1),(23,'Rijperkerkpark','MJS',_binary '',958,21,1),(24,'Koolhoven','MJS',_binary '',967,22,1),(25,'Bendastraat','MJS',_binary '',569,23,1),(26,'Bachlaan','MJS',_binary '',708,24,1),(27,'Verhulstlaan','MJS',_binary '',475,25,1),(28,'Udenhout','MJS',_binary '',575,26,1),(29,'Berkel-Enschot','MJS',_binary '',943,27,1);
/*!40000 ALTER TABLE `station` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `token`
--

DROP TABLE IF EXISTS `token`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `token` (
  `id` bigint(20) NOT NULL,
  `creation_time` datetime(6) DEFAULT NULL,
  `link_hash` varchar(255) DEFAULT NULL,
  `user_userid` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FKp2lrydh553poqd4jq5f2gxh5u` (`user_userid`),
  CONSTRAINT `FKp2lrydh553poqd4jq5f2gxh5u` FOREIGN KEY (`user_userid`) REFERENCES `user` (`userid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `token`
--

LOCK TABLES `token` WRITE;
/*!40000 ALTER TABLE `token` DISABLE KEYS */;
/*!40000 ALTER TABLE `token` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `userid` bigint(20) NOT NULL AUTO_INCREMENT,
  `admin` bit(1) NOT NULL,
  `first_name` varchar(255) DEFAULT NULL,
  `last_name` varchar(255) DEFAULT NULL,
  `mail_address` varchar(255) DEFAULT NULL,
  `user_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`userid`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,_binary '\0','Pieter','Peter','Pieter@mail.com','PieterPeter'),(2,_binary '','Jan','Joep','Jan@mail.com','JanJoep'),(3,_binary '\0','Joeri','waterman','Joeri@mail.com','JoeriWaterman'),(4,_binary '\0','Benny','Bener','Benny@mail.com','BennyBener'),(5,_binary '\0','Janny','Jansen','Janny@mail.com','JannyJansen');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 's3vj23'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-06-12 15:40:37
