-- MySQL dump 10.13  Distrib 8.0.45, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: new_yemen_looted_artefacts
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
-- Temporary view structure for view `looted_identified_artefacts`
--

DROP TABLE IF EXISTS `looted_identified_artefacts`;
/*!50001 DROP VIEW IF EXISTS `looted_identified_artefacts`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `looted_identified_artefacts` AS SELECT 
 1 AS `artifact_id`,
 1 AS `link`,
 1 AS `normalized_domain`,
 1 AS `city`,
 1 AS `country`,
 1 AS `source_classification`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `artefacts_scoring`
--

DROP TABLE IF EXISTS `artefacts_scoring`;
/*!50001 DROP VIEW IF EXISTS `artefacts_scoring`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `artefacts_scoring` AS SELECT 
 1 AS `artifact_id`,
 1 AS `score_txt`,
 1 AS `score_img`,
 1 AS `pdf_name`,
 1 AS `page_num`,
 1 AS `pdf_upgrd_description`,
 1 AS `wb_txt_lg`,
 1 AS `link`*/;
SET character_set_client = @saved_cs_client;

--
-- Final view structure for view `looted_identified_artefacts`
--

/*!50001 DROP VIEW IF EXISTS `looted_identified_artefacts`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `looted_identified_artefacts` AS select `w`.`artifact_id` AS `artifact_id`,`w`.`link` AS `link`,`a`.`normalized_domain` AS `normalized_domain`,`a`.`city` AS `city`,`a`.`country` AS `country`,`a`.`source_classification` AS `source_classification` from (`web_pages` `w` join `art_dealers` `a` on((`w`.`main_website` = `a`.`main_website`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `artefacts_scoring`
--

/*!50001 DROP VIEW IF EXISTS `artefacts_scoring`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `artefacts_scoring` AS select `ms`.`artifact_id` AS `artifact_id`,`ms`.`score_txt` AS `score_txt`,`ms`.`score_img` AS `score_img`,`l`.`pdf_name` AS `pdf_name`,`l`.`page_num` AS `page_num`,`l`.`pdf_upgrd_description` AS `pdf_upgrd_description`,`w`.`wb_txt_lg` AS `wb_txt_lg`,`w`.`link` AS `link` from ((`match_scoring` `ms` join `looted_artefacts` `l` on((`ms`.`artifact_id` = `l`.`artifact_id`))) join `web_pages` `w` on((`ms`.`artifact_id` = `w`.`artifact_id`))) where ((`w`.`link` is not null) and (trim(`w`.`link`) <> '')) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-27 20:18:30
