-- MySQL dump 10.13  Distrib 5.7.17, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: searchenginedb
-- ------------------------------------------------------
-- Server version	5.7.21-log

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
-- Table structure for table `idf`
--

DROP TABLE IF EXISTS `idf`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `idf` (
  `word` varchar(250) NOT NULL,
  `counts` decimal(6,2) DEFAULT NULL,
  PRIMARY KEY (`word`),
  CONSTRAINT `idf_ibfk_1` FOREIGN KEY (`word`) REFERENCES `tokens` (`word`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `idf`
--

LOCK TABLES `idf` WRITE;
/*!40000 ALTER TABLE `idf` DISABLE KEYS */;
/*!40000 ALTER TABLE `idf` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tokens`
--

DROP TABLE IF EXISTS `tokens`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tokens` (
  `word` varchar(250) NOT NULL,
  `term_frequency` int(11) DEFAULT NULL,
  `doc_id` int(11) NOT NULL,
  `tfandidf` int(11) DEFAULT NULL,
  PRIMARY KEY (`word`,`doc_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tokens`
--

LOCK TABLES `tokens` WRITE;
/*!40000 ALTER TABLE `tokens` DISABLE KEYS */;
/*!40000 ALTER TABLE `tokens` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'searchenginedb'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-05-10 21:55:04
