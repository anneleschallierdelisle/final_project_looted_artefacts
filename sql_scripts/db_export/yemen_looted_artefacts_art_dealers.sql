CREATE DATABASE  IF NOT EXISTS `yemen_looted_artefacts` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `yemen_looted_artefacts`;
-- MySQL dump 10.13  Distrib 8.0.45, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: yemen_looted_artefacts
-- ------------------------------------------------------
-- Server version	8.0.45

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `art_dealers`
--

DROP TABLE IF EXISTS `art_dealers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `art_dealers` (
  `main_website` varchar(255) NOT NULL,
  `normalized_domain` varchar(255) DEFAULT NULL,
  `city` varchar(255) DEFAULT NULL,
  `country` varchar(255) DEFAULT NULL,
  `source_classification` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`main_website`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `art_dealers`
--

LOCK TABLES `art_dealers` WRITE;
/*!40000 ALTER TABLE `art_dealers` DISABLE KEYS */;
INSERT INTO `art_dealers` VALUES ('1stdibs.com','1stdibs.com','New York','USA','marketplace'),('acropolo.com','acropolo.com','Sharjah','United Arab Emirates','dealer'),('ancient-agate-jasper-carnelian-asiatic-eastern','ancient-agate-jasper-carnelian-asiatic-eastern','Unknown','Unknown','unknown'),('ancient-art.co.uk','ancient-art.co.uk','London','UK','dealer'),('ancient-dromedary-bronze-arabian-eastern','ancient-dromedary-bronze-arabian-eastern','Unknown','Unknown','unknown'),('antiquities.co.uk','antiquities.co.uk','London','UK','dealer'),('art.thewalters.org','thewalters.org','Baltimore','USA','museum'),('artandantiquities.co.uk','artandantiquities.co.uk','London','UK','dealer'),('artcurial.com','artcurial.com','Paris','France','auction'),('artemission.com','artemission.com','London','UK','auction'),('atharsale.com','atharsale.com','Riyadh','Saudi Arabia','auction'),('bada.org','bada.org','London','UK','association'),('barakatgallery.com','barakatgallery.com','London','UK','dealer'),('bertolamifineart.bidinside.com','bidinside.com','Unknown','Italy','platform'),('bid.curatedauctions.co.uk','bid.curatedauctions.co.uk','London','UK','auction'),('bidsquare.com','bidsquare.com','New York','USA','platform'),('bonhams.com','bonhams.com','London','UK','auction'),('britishmuseum.org','britishmuseum.org','London','UK','museum'),('christies.com','christies.com','London','UK','auction'),('collections.louvre.fr','louvre.fr','Paris','France','museum'),('dasi.cnr.it','dasi.cnr.it','Unknown','Italy','academic'),('davidaaron.com','davidaaron.com','London','UK','dealer'),('discountsonline.cheap2022.ru','discountsonline.cheap2022.ru','Unknown','Russia','unknown'),('drouot.com','drouot.com','Paris','France','auction'),('e-south-arrivals','e-south-arrivals','Unknown','Unknown','unknown'),('e-tiquities.com','e-tiquities.com','Unknown','Unknown','unknown'),('ebay.com','ebay.com','San Jose','USA','marketplace'),('freemansauction.com','freemansauction.com','Philadelphia','USA','auction'),('georgeortiz.com','georgeortiz.com','Geneva','Switzerland','collection'),('heidicon.ub.uni-heidelberg.de','ub.uni-heidelberg.de','Heidelberg','Germany','academic'),('hindmanauctions.com','hindmanauctions.com','Chicago','USA','auction'),('il..com','il..com','Unknown','Unknown','unknown'),('il.bidspirit.com','bidspirit.com','Tel Aviv','Israel','platform'),('images.ashmolean.org','ashmolean.org','Oxford','UK','museum'),('invaluable.com','invaluable.com','Boston','USA','platform'),('jenikirbyhistory.getarchive.net','getarchive.net','Unknown','USA','archive'),('kedem-auctions.com','kedem-auctions.com','Jerusalem','Israel','auction'),('khm.at','khm.at','Vienna','Austria','museum'),('lapada.org','lapada.org','London','UK','association'),('liveauctioneers.com','liveauctioneers.com','New York','USA','platform'),('lot-ancient-near-east-art.com','lot-ancient-near-east-art.com','Unknown','Unknown','unknown'),('lot-ancient-south-art.com','lot-ancient-south-art.com','Unknown','Unknown','unknown'),('lot-arabian-south-arabian-weight','lot-arabian-south-arabian-weight','Unknown','Unknown','unknown'),('lot-archaeological-south-arabian-bowl','lot-archaeological-south-arabian-bowl','Unknown','Unknown','unknown'),('lot-art.com','lot-art.com','Amsterdam','Netherlands','platform'),('lot-kingdom_sheba-art.com','lot-kingdom_sheba-art.com','Manchester','UK','unknown'),('lotapollo17.12.23-south_arabian-camel','lotapollo17.12.23-south_arabian-camel','Unknown','Unknown','unknown'),('lotcatawiki-27.1.23-bead_34-century','lotcatawiki-27.1.23-bead_34-century','Unknown','Unknown','unknown'),('lyonandturnbull.com','lyonandturnbull.com','Edinburgh','UK','auction'),('martindoustar.com','martindoustar.com','London','UK','dealer'),('metmuseum.org','metmuseum.org','New York','USA','museum'),('n9.cl','n9.cl','Unknown','Unknown','unknown'),('nm.gov.om','nm.gov.om','Muscat','Oman','institution'),('orientalartauctions.com','orientalartauctions.com','Unknown','UK','auction'),('pba-auctions.com','pba-auctions.com','Unknown','USA','auction'),('pbaons.com','pbaons.com','Unknown','Unknown','unknown'),('phoenixancientart.com','phoenixancientart.com','Geneva','Switzerland','dealer'),('sa24.co ','sa24.co','Unknown','Yemen','media'),('sothebys.com','sothebys.com','London','UK','auction'),('the-saleroom.com','the-saleroom.com','London','UK','platform'),('thecityreview.com','thecityreview.com','Unknown','Unknown','media'),('timesofisrael.com','timesofisrael.com','Jerusalem','Israel','media'),('traveltoeat.com','traveltoeat.com','Unknown','Unknown','unknown'),('zacke.at','zacke.at','Vienna','Austria','auction');
/*!40000 ALTER TABLE `art_dealers` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-13 23:25:31
