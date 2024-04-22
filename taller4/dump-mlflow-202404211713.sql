-- MySQL dump 10.13  Distrib 8.0.32, for Win64 (x86_64)
--
-- Host: 10.43.101.156    Database: mlflow
-- ------------------------------------------------------
-- Server version	8.3.0

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
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('3500859a5d39');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `experiment_tags`
--

DROP TABLE IF EXISTS `experiment_tags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `experiment_tags` (
  `key` varchar(250) NOT NULL,
  `value` varchar(5000) DEFAULT NULL,
  `experiment_id` int NOT NULL,
  PRIMARY KEY (`key`,`experiment_id`),
  KEY `experiment_id` (`experiment_id`),
  CONSTRAINT `experiment_tags_ibfk_1` FOREIGN KEY (`experiment_id`) REFERENCES `experiments` (`experiment_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `experiment_tags`
--

LOCK TABLES `experiment_tags` WRITE;
/*!40000 ALTER TABLE `experiment_tags` DISABLE KEYS */;
/*!40000 ALTER TABLE `experiment_tags` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `experiments`
--

DROP TABLE IF EXISTS `experiments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `experiments` (
  `experiment_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(256) NOT NULL,
  `artifact_location` varchar(256) DEFAULT NULL,
  `lifecycle_stage` varchar(32) DEFAULT NULL,
  `creation_time` bigint DEFAULT NULL,
  `last_update_time` bigint DEFAULT NULL,
  PRIMARY KEY (`experiment_id`),
  UNIQUE KEY `name` (`name`),
  CONSTRAINT `experiments_lifecycle_stage` CHECK ((`lifecycle_stage` in (_utf8mb4'active',_utf8mb4'deleted')))
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `experiments`
--

LOCK TABLES `experiments` WRITE;
/*!40000 ALTER TABLE `experiments` DISABLE KEYS */;
INSERT INTO `experiments` VALUES (0,'Default','s3://mlflows3/0','deleted',1712286105586,1712371270461),(1,'mlflow_tracking','s3://mlflows3/1','active',1712287278581,1712287278581);
/*!40000 ALTER TABLE `experiments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `latest_metrics`
--

DROP TABLE IF EXISTS `latest_metrics`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `latest_metrics` (
  `key` varchar(250) NOT NULL,
  `value` double NOT NULL,
  `timestamp` bigint DEFAULT NULL,
  `step` bigint NOT NULL,
  `is_nan` tinyint(1) NOT NULL,
  `run_uuid` varchar(32) NOT NULL,
  PRIMARY KEY (`key`,`run_uuid`),
  KEY `index_latest_metrics_run_uuid` (`run_uuid`),
  CONSTRAINT `latest_metrics_ibfk_1` FOREIGN KEY (`run_uuid`) REFERENCES `runs` (`run_uuid`),
  CONSTRAINT `latest_metrics_chk_1` CHECK ((`is_nan` in (0,1)))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `latest_metrics`
--

LOCK TABLES `latest_metrics` WRITE;
/*!40000 ALTER TABLE `latest_metrics` DISABLE KEYS */;
INSERT INTO `latest_metrics` VALUES ('accuracy',0.9480207021571444,1712430101145,0,0,'13253df6287a46da9e58de0db31f2993'),('accuracy',0.8981640849110729,1712287281639,0,0,'1c858e176dff4d72acc0787fee7b5b1d'),('accuracy',0.9480207021571444,1712540887610,0,0,'2377c988458446db8be230afca1cbea3'),('accuracy',0.8981640849110729,1712288572129,0,0,'269d3b734c14417db8df169fd8b1440f'),('accuracy',0.8981640849110729,1712289278378,0,0,'34e74b048bc74981b6ebfddc62524461'),('accuracy',0.9398409966396196,1712371778768,0,0,'3ab0948239c74a78bf8d82176fa4f996'),('accuracy',0.9440008843389855,1712421370803,0,0,'4cb5283913974b72895d53e0c230989e'),('accuracy',0.9480207021571444,1712430925343,0,0,'5242254aee3c4c48917a198e012b145c'),('accuracy',0.9398409966396196,1712376919577,0,0,'60c7bc3ddcc84815adf8ccbe68b1f0be'),('accuracy',0.9122203098106713,1712368990130,0,0,'61bf01c99c3e43c7ad62dddb0d6f79d5'),('accuracy',0.9480207021571444,1712540888140,0,0,'7062f65b8103479392c092efaaa4ad15'),('accuracy',0.9398409966396196,1712371207942,0,0,'75ceaeca37c64a16b6728e6ca37fc105'),('accuracy',0.8981640849110729,1712289511315,0,0,'75dcda9566ba44a682adec6514139fb5'),('accuracy',0.9440008843389855,1712424538216,0,0,'8a3ff5c275e74facbf12a73efcc759fe'),('accuracy',0.8981640849110729,1712290386798,0,0,'9b13d777c0a34fda8751552723a20bf6'),('accuracy',0.9480207021571444,1712430098114,0,0,'adeb210dde6e4e27a254c20ffdfcb7da'),('accuracy',0.8981640849110729,1712287916307,0,0,'b86132597fcf49959a83fddab6b94198'),('accuracy',0.9398409966396196,1712377496942,0,0,'f77cf7308e80493b94398a85be68a209'),('accuracy',0.9122203098106713,1712370003273,0,0,'ff3c7b58f2774afab7b7e3c389a3b710'),('f1_score',0.9563953666944625,1712430101287,0,0,'13253df6287a46da9e58de0db31f2993'),('f1_score',0.9563953666944625,1712540887699,0,0,'2377c988458446db8be230afca1cbea3'),('f1_score',0.945373266135766,1712371778850,0,0,'3ab0948239c74a78bf8d82176fa4f996'),('f1_score',0.95498726478374,1712421371040,0,0,'4cb5283913974b72895d53e0c230989e'),('f1_score',0.9563953666944625,1712430925414,0,0,'5242254aee3c4c48917a198e012b145c'),('f1_score',0.945373266135766,1712376919679,0,0,'60c7bc3ddcc84815adf8ccbe68b1f0be'),('f1_score',0.9563953666944625,1712540888216,0,0,'7062f65b8103479392c092efaaa4ad15'),('f1_score',0.945373266135766,1712371208049,0,0,'75ceaeca37c64a16b6728e6ca37fc105'),('f1_score',0.95498726478374,1712424538306,0,0,'8a3ff5c275e74facbf12a73efcc759fe'),('f1_score',0.9563953666944625,1712430098250,0,0,'adeb210dde6e4e27a254c20ffdfcb7da'),('f1_score',0.945373266135766,1712377497049,0,0,'f77cf7308e80493b94398a85be68a209'),('precision',0.9563699482040824,1712430101190,0,0,'13253df6287a46da9e58de0db31f2993'),('precision',0.9563699482040824,1712540887636,0,0,'2377c988458446db8be230afca1cbea3'),('precision',0.9453031532135746,1712371778788,0,0,'3ab0948239c74a78bf8d82176fa4f996'),('precision',0.9550554947373322,1712421370964,0,0,'4cb5283913974b72895d53e0c230989e'),('precision',0.9563699482040824,1712430925370,0,0,'5242254aee3c4c48917a198e012b145c'),('precision',0.9453031532135746,1712376919618,0,0,'60c7bc3ddcc84815adf8ccbe68b1f0be'),('precision',0.9563699482040824,1712540888165,0,0,'7062f65b8103479392c092efaaa4ad15'),('precision',0.9453031532135746,1712371207990,0,0,'75ceaeca37c64a16b6728e6ca37fc105'),('precision',0.9550554947373322,1712424538251,0,0,'8a3ff5c275e74facbf12a73efcc759fe'),('precision',0.9563699482040824,1712430098151,0,0,'adeb210dde6e4e27a254c20ffdfcb7da'),('precision',0.9453031532135746,1712377496975,0,0,'f77cf7308e80493b94398a85be68a209'),('recall',0.9565117613310384,1712430101257,0,0,'13253df6287a46da9e58de0db31f2993'),('recall',0.9565117613310384,1712540887669,0,0,'2377c988458446db8be230afca1cbea3'),('recall',0.9454962707974757,1712371778819,0,0,'3ab0948239c74a78bf8d82176fa4f996'),('recall',0.9549627079747561,1712421370995,0,0,'4cb5283913974b72895d53e0c230989e'),('recall',0.9565117613310384,1712430925393,0,0,'5242254aee3c4c48917a198e012b145c'),('recall',0.9454962707974757,1712376919651,0,0,'60c7bc3ddcc84815adf8ccbe68b1f0be'),('recall',0.9565117613310384,1712540888191,0,0,'7062f65b8103479392c092efaaa4ad15'),('recall',0.9454962707974757,1712371208021,0,0,'75ceaeca37c64a16b6728e6ca37fc105'),('recall',0.9549627079747561,1712424538281,0,0,'8a3ff5c275e74facbf12a73efcc759fe'),('recall',0.9565117613310384,1712430098216,0,0,'adeb210dde6e4e27a254c20ffdfcb7da'),('recall',0.9454962707974757,1712377497019,0,0,'f77cf7308e80493b94398a85be68a209');
/*!40000 ALTER TABLE `latest_metrics` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `metrics`
--

DROP TABLE IF EXISTS `metrics`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `metrics` (
  `key` varchar(250) NOT NULL,
  `value` double NOT NULL,
  `timestamp` bigint NOT NULL,
  `run_uuid` varchar(32) NOT NULL,
  `step` bigint NOT NULL DEFAULT '0',
  `is_nan` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`key`,`timestamp`,`step`,`run_uuid`,`value`,`is_nan`),
  KEY `index_metrics_run_uuid` (`run_uuid`),
  CONSTRAINT `metrics_ibfk_1` FOREIGN KEY (`run_uuid`) REFERENCES `runs` (`run_uuid`),
  CONSTRAINT `metrics_chk_1` CHECK ((`is_nan` in (0,1))),
  CONSTRAINT `metrics_chk_2` CHECK ((`is_nan` in (0,1)))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `metrics`
--

LOCK TABLES `metrics` WRITE;
/*!40000 ALTER TABLE `metrics` DISABLE KEYS */;
INSERT INTO `metrics` VALUES ('accuracy',0.9480207021571444,1712430101145,'13253df6287a46da9e58de0db31f2993',0,0),('f1_score',0.9563953666944625,1712430101287,'13253df6287a46da9e58de0db31f2993',0,0),('precision',0.9563699482040824,1712430101190,'13253df6287a46da9e58de0db31f2993',0,0),('recall',0.9565117613310384,1712430101257,'13253df6287a46da9e58de0db31f2993',0,0),('accuracy',0.8981640849110729,1712287281639,'1c858e176dff4d72acc0787fee7b5b1d',0,0),('accuracy',0.9480207021571444,1712540887610,'2377c988458446db8be230afca1cbea3',0,0),('f1_score',0.9563953666944625,1712540887699,'2377c988458446db8be230afca1cbea3',0,0),('precision',0.9563699482040824,1712540887636,'2377c988458446db8be230afca1cbea3',0,0),('recall',0.9565117613310384,1712540887669,'2377c988458446db8be230afca1cbea3',0,0),('accuracy',0.8981640849110729,1712288572129,'269d3b734c14417db8df169fd8b1440f',0,0),('accuracy',0.8981640849110729,1712289278378,'34e74b048bc74981b6ebfddc62524461',0,0),('accuracy',0.9398409966396196,1712371778768,'3ab0948239c74a78bf8d82176fa4f996',0,0),('f1_score',0.945373266135766,1712371778850,'3ab0948239c74a78bf8d82176fa4f996',0,0),('precision',0.9453031532135746,1712371778788,'3ab0948239c74a78bf8d82176fa4f996',0,0),('recall',0.9454962707974757,1712371778819,'3ab0948239c74a78bf8d82176fa4f996',0,0),('accuracy',0.9440008843389855,1712421370803,'4cb5283913974b72895d53e0c230989e',0,0),('f1_score',0.95498726478374,1712421371040,'4cb5283913974b72895d53e0c230989e',0,0),('precision',0.9550554947373322,1712421370964,'4cb5283913974b72895d53e0c230989e',0,0),('recall',0.9549627079747561,1712421370995,'4cb5283913974b72895d53e0c230989e',0,0),('accuracy',0.9480207021571444,1712430925343,'5242254aee3c4c48917a198e012b145c',0,0),('f1_score',0.9563953666944625,1712430925414,'5242254aee3c4c48917a198e012b145c',0,0),('precision',0.9563699482040824,1712430925370,'5242254aee3c4c48917a198e012b145c',0,0),('recall',0.9565117613310384,1712430925393,'5242254aee3c4c48917a198e012b145c',0,0),('accuracy',0.9398409966396196,1712376919577,'60c7bc3ddcc84815adf8ccbe68b1f0be',0,0),('f1_score',0.945373266135766,1712376919679,'60c7bc3ddcc84815adf8ccbe68b1f0be',0,0),('precision',0.9453031532135746,1712376919618,'60c7bc3ddcc84815adf8ccbe68b1f0be',0,0),('recall',0.9454962707974757,1712376919651,'60c7bc3ddcc84815adf8ccbe68b1f0be',0,0),('accuracy',0.9122203098106713,1712368990130,'61bf01c99c3e43c7ad62dddb0d6f79d5',0,0),('accuracy',0.9480207021571444,1712540888140,'7062f65b8103479392c092efaaa4ad15',0,0),('f1_score',0.9563953666944625,1712540888216,'7062f65b8103479392c092efaaa4ad15',0,0),('precision',0.9563699482040824,1712540888165,'7062f65b8103479392c092efaaa4ad15',0,0),('recall',0.9565117613310384,1712540888191,'7062f65b8103479392c092efaaa4ad15',0,0),('accuracy',0.9398409966396196,1712371207942,'75ceaeca37c64a16b6728e6ca37fc105',0,0),('f1_score',0.945373266135766,1712371208049,'75ceaeca37c64a16b6728e6ca37fc105',0,0),('precision',0.9453031532135746,1712371207990,'75ceaeca37c64a16b6728e6ca37fc105',0,0),('recall',0.9454962707974757,1712371208021,'75ceaeca37c64a16b6728e6ca37fc105',0,0),('accuracy',0.8981640849110729,1712289511315,'75dcda9566ba44a682adec6514139fb5',0,0),('accuracy',0.9440008843389855,1712424538216,'8a3ff5c275e74facbf12a73efcc759fe',0,0),('f1_score',0.95498726478374,1712424538306,'8a3ff5c275e74facbf12a73efcc759fe',0,0),('precision',0.9550554947373322,1712424538251,'8a3ff5c275e74facbf12a73efcc759fe',0,0),('recall',0.9549627079747561,1712424538281,'8a3ff5c275e74facbf12a73efcc759fe',0,0),('accuracy',0.8981640849110729,1712290386798,'9b13d777c0a34fda8751552723a20bf6',0,0),('accuracy',0.9480207021571444,1712430098114,'adeb210dde6e4e27a254c20ffdfcb7da',0,0),('f1_score',0.9563953666944625,1712430098250,'adeb210dde6e4e27a254c20ffdfcb7da',0,0),('precision',0.9563699482040824,1712430098151,'adeb210dde6e4e27a254c20ffdfcb7da',0,0),('recall',0.9565117613310384,1712430098216,'adeb210dde6e4e27a254c20ffdfcb7da',0,0),('accuracy',0.8981640849110729,1712287916307,'b86132597fcf49959a83fddab6b94198',0,0),('accuracy',0.9398409966396196,1712377496942,'f77cf7308e80493b94398a85be68a209',0,0),('f1_score',0.945373266135766,1712377497049,'f77cf7308e80493b94398a85be68a209',0,0),('precision',0.9453031532135746,1712377496975,'f77cf7308e80493b94398a85be68a209',0,0),('recall',0.9454962707974757,1712377497019,'f77cf7308e80493b94398a85be68a209',0,0),('accuracy',0.9122203098106713,1712370003273,'ff3c7b58f2774afab7b7e3c389a3b710',0,0);
/*!40000 ALTER TABLE `metrics` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `model_version_tags`
--

DROP TABLE IF EXISTS `model_version_tags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `model_version_tags` (
  `key` varchar(250) NOT NULL,
  `value` varchar(5000) DEFAULT NULL,
  `name` varchar(256) NOT NULL,
  `version` int NOT NULL,
  PRIMARY KEY (`key`,`name`,`version`),
  KEY `name` (`name`,`version`),
  CONSTRAINT `model_version_tags_ibfk_1` FOREIGN KEY (`name`, `version`) REFERENCES `model_versions` (`name`, `version`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `model_version_tags`
--

LOCK TABLES `model_version_tags` WRITE;
/*!40000 ALTER TABLE `model_version_tags` DISABLE KEYS */;
/*!40000 ALTER TABLE `model_version_tags` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `model_versions`
--

DROP TABLE IF EXISTS `model_versions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `model_versions` (
  `name` varchar(256) NOT NULL,
  `version` int NOT NULL,
  `creation_time` bigint DEFAULT NULL,
  `last_updated_time` bigint DEFAULT NULL,
  `description` varchar(5000) DEFAULT NULL,
  `user_id` varchar(256) DEFAULT NULL,
  `current_stage` varchar(20) DEFAULT NULL,
  `source` varchar(500) DEFAULT NULL,
  `run_id` varchar(32) DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  `status_message` varchar(500) DEFAULT NULL,
  `run_link` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`name`,`version`),
  CONSTRAINT `model_versions_ibfk_1` FOREIGN KEY (`name`) REFERENCES `registered_models` (`name`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `model_versions`
--

LOCK TABLES `model_versions` WRITE;
/*!40000 ALTER TABLE `model_versions` DISABLE KEYS */;
INSERT INTO `model_versions` VALUES ('cover_type_class',1,1712376926804,1712376926804,'',NULL,'None','s3://mlflows3/1/60c7bc3ddcc84815adf8ccbe68b1f0be/artifacts/model','60c7bc3ddcc84815adf8ccbe68b1f0be','READY',NULL,''),('cover_type_class',2,1712377502552,1712377502552,'',NULL,'None','s3://mlflows3/1/f77cf7308e80493b94398a85be68a209/artifacts/model','f77cf7308e80493b94398a85be68a209','READY',NULL,''),('cover_type_class',3,1712421376637,1712421376637,'',NULL,'None','s3://mlflows3/1/4cb5283913974b72895d53e0c230989e/artifacts/model','4cb5283913974b72895d53e0c230989e','READY',NULL,''),('cover_type_class',4,1712424544283,1712424544283,'',NULL,'None','s3://mlflows3/1/8a3ff5c275e74facbf12a73efcc759fe/artifacts/model','8a3ff5c275e74facbf12a73efcc759fe','READY',NULL,''),('cover_type_class',5,1712430107629,1712430107629,'',NULL,'None','s3://mlflows3/1/adeb210dde6e4e27a254c20ffdfcb7da/artifacts/model','adeb210dde6e4e27a254c20ffdfcb7da','READY',NULL,''),('cover_type_class',6,1712430930490,1712430930490,'',NULL,'None','s3://mlflows3/1/5242254aee3c4c48917a198e012b145c/artifacts/model','5242254aee3c4c48917a198e012b145c','READY',NULL,''),('cover_type_class',7,1712540893787,1712540893787,'',NULL,'None','s3://mlflows3/1/7062f65b8103479392c092efaaa4ad15/artifacts/model','7062f65b8103479392c092efaaa4ad15','READY',NULL,''),('cover_type_class',8,1712540893825,1712540893825,'',NULL,'None','s3://mlflows3/1/2377c988458446db8be230afca1cbea3/artifacts/model','2377c988458446db8be230afca1cbea3','READY',NULL,'');
/*!40000 ALTER TABLE `model_versions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `params`
--

DROP TABLE IF EXISTS `params`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `params` (
  `key` varchar(250) NOT NULL,
  `value` varchar(500) NOT NULL,
  `run_uuid` varchar(32) NOT NULL,
  PRIMARY KEY (`key`,`run_uuid`),
  KEY `index_params_run_uuid` (`run_uuid`),
  CONSTRAINT `params_ibfk_1` FOREIGN KEY (`run_uuid`) REFERENCES `runs` (`run_uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `params`
--

LOCK TABLES `params` WRITE;
/*!40000 ALTER TABLE `params` DISABLE KEYS */;
INSERT INTO `params` VALUES ('SVM__C','83','13253df6287a46da9e58de0db31f2993'),('SVM__C','83','2377c988458446db8be230afca1cbea3'),('SVM__C','83','3ab0948239c74a78bf8d82176fa4f996'),('SVM__C','83','4cb5283913974b72895d53e0c230989e'),('SVM__C','83','5242254aee3c4c48917a198e012b145c'),('SVM__C','83','60c7bc3ddcc84815adf8ccbe68b1f0be'),('SVM__C','83','7062f65b8103479392c092efaaa4ad15'),('SVM__C','83','75ceaeca37c64a16b6728e6ca37fc105'),('SVM__C','83','8a3ff5c275e74facbf12a73efcc759fe'),('SVM__C','83','adeb210dde6e4e27a254c20ffdfcb7da'),('SVM__C','83','f77cf7308e80493b94398a85be68a209'),('SVM__gamma','scale','13253df6287a46da9e58de0db31f2993'),('SVM__gamma','scale','2377c988458446db8be230afca1cbea3'),('SVM__gamma','scale','3ab0948239c74a78bf8d82176fa4f996'),('SVM__gamma','scale','4cb5283913974b72895d53e0c230989e'),('SVM__gamma','scale','5242254aee3c4c48917a198e012b145c'),('SVM__gamma','scale','60c7bc3ddcc84815adf8ccbe68b1f0be'),('SVM__gamma','scale','7062f65b8103479392c092efaaa4ad15'),('SVM__gamma','scale','75ceaeca37c64a16b6728e6ca37fc105'),('SVM__gamma','scale','8a3ff5c275e74facbf12a73efcc759fe'),('SVM__gamma','scale','adeb210dde6e4e27a254c20ffdfcb7da'),('SVM__gamma','scale','f77cf7308e80493b94398a85be68a209'),('SVM__kernel','rbf','13253df6287a46da9e58de0db31f2993'),('SVM__kernel','rbf','2377c988458446db8be230afca1cbea3'),('SVM__kernel','rbf','3ab0948239c74a78bf8d82176fa4f996'),('SVM__kernel','rbf','4cb5283913974b72895d53e0c230989e'),('SVM__kernel','rbf','5242254aee3c4c48917a198e012b145c'),('SVM__kernel','rbf','60c7bc3ddcc84815adf8ccbe68b1f0be'),('SVM__kernel','rbf','7062f65b8103479392c092efaaa4ad15'),('SVM__kernel','rbf','75ceaeca37c64a16b6728e6ca37fc105'),('SVM__kernel','rbf','8a3ff5c275e74facbf12a73efcc759fe'),('SVM__kernel','rbf','adeb210dde6e4e27a254c20ffdfcb7da'),('SVM__kernel','rbf','f77cf7308e80493b94398a85be68a209');
/*!40000 ALTER TABLE `params` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `registered_model_aliases`
--

DROP TABLE IF EXISTS `registered_model_aliases`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `registered_model_aliases` (
  `alias` varchar(256) NOT NULL,
  `version` int NOT NULL,
  `name` varchar(256) NOT NULL,
  PRIMARY KEY (`name`,`alias`),
  CONSTRAINT `registered_model_alias_name_fkey` FOREIGN KEY (`name`) REFERENCES `registered_models` (`name`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `registered_model_aliases`
--

LOCK TABLES `registered_model_aliases` WRITE;
/*!40000 ALTER TABLE `registered_model_aliases` DISABLE KEYS */;
/*!40000 ALTER TABLE `registered_model_aliases` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `registered_model_tags`
--

DROP TABLE IF EXISTS `registered_model_tags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `registered_model_tags` (
  `key` varchar(250) NOT NULL,
  `value` varchar(5000) DEFAULT NULL,
  `name` varchar(256) NOT NULL,
  PRIMARY KEY (`key`,`name`),
  KEY `name` (`name`),
  CONSTRAINT `registered_model_tags_ibfk_1` FOREIGN KEY (`name`) REFERENCES `registered_models` (`name`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `registered_model_tags`
--

LOCK TABLES `registered_model_tags` WRITE;
/*!40000 ALTER TABLE `registered_model_tags` DISABLE KEYS */;
/*!40000 ALTER TABLE `registered_model_tags` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `registered_models`
--

DROP TABLE IF EXISTS `registered_models`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `registered_models` (
  `name` varchar(256) NOT NULL,
  `creation_time` bigint DEFAULT NULL,
  `last_updated_time` bigint DEFAULT NULL,
  `description` varchar(5000) DEFAULT NULL,
  PRIMARY KEY (`name`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `registered_models`
--

LOCK TABLES `registered_models` WRITE;
/*!40000 ALTER TABLE `registered_models` DISABLE KEYS */;
INSERT INTO `registered_models` VALUES ('cover_type_class',1712376926613,1712540893825,'');
/*!40000 ALTER TABLE `registered_models` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `runs`
--

DROP TABLE IF EXISTS `runs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `runs` (
  `run_uuid` varchar(32) NOT NULL,
  `name` varchar(250) DEFAULT NULL,
  `source_type` varchar(20) DEFAULT NULL,
  `source_name` varchar(500) DEFAULT NULL,
  `entry_point_name` varchar(50) DEFAULT NULL,
  `user_id` varchar(256) DEFAULT NULL,
  `status` varchar(9) DEFAULT NULL,
  `start_time` bigint DEFAULT NULL,
  `end_time` bigint DEFAULT NULL,
  `source_version` varchar(50) DEFAULT NULL,
  `lifecycle_stage` varchar(20) DEFAULT NULL,
  `artifact_uri` varchar(200) DEFAULT NULL,
  `experiment_id` int DEFAULT NULL,
  `deleted_time` bigint DEFAULT NULL,
  PRIMARY KEY (`run_uuid`),
  KEY `experiment_id` (`experiment_id`),
  CONSTRAINT `runs_ibfk_1` FOREIGN KEY (`experiment_id`) REFERENCES `experiments` (`experiment_id`),
  CONSTRAINT `runs_chk_1` CHECK ((`status` in (_utf8mb4'SCHEDULED',_utf8mb4'FAILED',_utf8mb4'FINISHED',_utf8mb4'RUNNING',_utf8mb4'KILLED'))),
  CONSTRAINT `runs_lifecycle_stage` CHECK ((`lifecycle_stage` in (_utf8mb4'active',_utf8mb4'deleted'))),
  CONSTRAINT `source_type` CHECK ((`source_type` in (_utf8mb4'NOTEBOOK',_utf8mb4'JOB',_utf8mb4'LOCAL',_utf8mb4'UNKNOWN',_utf8mb4'PROJECT')))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `runs`
--

LOCK TABLES `runs` WRITE;
/*!40000 ALTER TABLE `runs` DISABLE KEYS */;
INSERT INTO `runs` VALUES ('13253df6287a46da9e58de0db31f2993','cover_type_class','UNKNOWN','','','root','FAILED',1712430101041,1712430107683,'','deleted','s3://mlflows3/1/13253df6287a46da9e58de0db31f2993/artifacts',1,1712431109354),('1c858e176dff4d72acc0787fee7b5b1d','test_1','UNKNOWN','','','root','FAILED',1712287278737,1712287289861,'','deleted','s3://mlflows3/1/1c858e176dff4d72acc0787fee7b5b1d/artifacts',1,1712289287647),('2377c988458446db8be230afca1cbea3','cover_type_class','UNKNOWN','','','root','FINISHED',1712540887543,1712540893860,'','active','s3://mlflows3/1/2377c988458446db8be230afca1cbea3/artifacts',1,NULL),('269d3b734c14417db8df169fd8b1440f','test_1','UNKNOWN','','','root','FAILED',1712288569097,1712288579999,'','deleted','s3://mlflows3/1/269d3b734c14417db8df169fd8b1440f/artifacts',1,1712289287637),('34e74b048bc74981b6ebfddc62524461','test_1','UNKNOWN','','','root','FINISHED',1712289275031,1712289283848,'','active','s3://mlflows3/1/34e74b048bc74981b6ebfddc62524461/artifacts',1,NULL),('3ab0948239c74a78bf8d82176fa4f996','cover_type_class','UNKNOWN','','','root','FINISHED',1712371778677,1712371784135,'','active','s3://mlflows3/1/3ab0948239c74a78bf8d82176fa4f996/artifacts',1,NULL),('4cb5283913974b72895d53e0c230989e','cover_type_class','UNKNOWN','','','root','FINISHED',1712421370741,1712421376791,'','active','s3://mlflows3/1/4cb5283913974b72895d53e0c230989e/artifacts',1,NULL),('5242254aee3c4c48917a198e012b145c','cover_type_class','UNKNOWN','','','root','FINISHED',1712430925254,1712430930517,'','active','s3://mlflows3/1/5242254aee3c4c48917a198e012b145c/artifacts',1,NULL),('60c7bc3ddcc84815adf8ccbe68b1f0be','cover_type_class','UNKNOWN','','','root','FINISHED',1712376919254,1712376926825,'','active','s3://mlflows3/1/60c7bc3ddcc84815adf8ccbe68b1f0be/artifacts',1,NULL),('61bf01c99c3e43c7ad62dddb0d6f79d5','test_1','UNKNOWN','','','root','FINISHED',1712368983907,1712368996818,'','deleted','s3://mlflows3/1/61bf01c99c3e43c7ad62dddb0d6f79d5/artifacts',1,1712421829654),('7062f65b8103479392c092efaaa4ad15','cover_type_class','UNKNOWN','','','root','FINISHED',1712540888048,1712540893831,'','active','s3://mlflows3/1/7062f65b8103479392c092efaaa4ad15/artifacts',1,NULL),('75ceaeca37c64a16b6728e6ca37fc105','cover_type_class','UNKNOWN','','','root','FINISHED',1712371207848,1712371214273,'','active','s3://mlflows3/1/75ceaeca37c64a16b6728e6ca37fc105/artifacts',1,NULL),('75dcda9566ba44a682adec6514139fb5','test_1','UNKNOWN','','','root','FINISHED',1712289508625,1712289517011,'','deleted','s3://mlflows3/1/75dcda9566ba44a682adec6514139fb5/artifacts',1,1712421829654),('8a3ff5c275e74facbf12a73efcc759fe','cover_type_class','UNKNOWN','','','root','FINISHED',1712424538090,1712424544309,'','active','s3://mlflows3/1/8a3ff5c275e74facbf12a73efcc759fe/artifacts',1,NULL),('9b13d777c0a34fda8751552723a20bf6','test_1','UNKNOWN','','','root','FINISHED',1712290383278,1712290392983,'','deleted','s3://mlflows3/1/9b13d777c0a34fda8751552723a20bf6/artifacts',1,1712421829655),('adeb210dde6e4e27a254c20ffdfcb7da','cover_type_class','UNKNOWN','','','root','FINISHED',1712430097990,1712430107671,'','active','s3://mlflows3/1/adeb210dde6e4e27a254c20ffdfcb7da/artifacts',1,NULL),('b86132597fcf49959a83fddab6b94198','test_1','UNKNOWN','','','root','FAILED',1712287912784,1712287925796,'','deleted','s3://mlflows3/1/b86132597fcf49959a83fddab6b94198/artifacts',1,1712289287649),('f77cf7308e80493b94398a85be68a209','cover_type_class','UNKNOWN','','','root','FINISHED',1712377496789,1712377502586,'','active','s3://mlflows3/1/f77cf7308e80493b94398a85be68a209/artifacts',1,NULL),('ff3c7b58f2774afab7b7e3c389a3b710','test_1','UNKNOWN','','','root','FINISHED',1712369997451,1712370008417,'','deleted','s3://mlflows3/1/ff3c7b58f2774afab7b7e3c389a3b710/artifacts',1,1712421829653);
/*!40000 ALTER TABLE `runs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tags`
--

DROP TABLE IF EXISTS `tags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tags` (
  `key` varchar(250) NOT NULL,
  `value` varchar(5000) DEFAULT NULL,
  `run_uuid` varchar(32) NOT NULL,
  PRIMARY KEY (`key`,`run_uuid`),
  KEY `index_tags_run_uuid` (`run_uuid`),
  CONSTRAINT `tags_ibfk_1` FOREIGN KEY (`run_uuid`) REFERENCES `runs` (`run_uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tags`
--

LOCK TABLES `tags` WRITE;
/*!40000 ALTER TABLE `tags` DISABLE KEYS */;
INSERT INTO `tags` VALUES ('mlflow.log-model.history','[{\"run_id\": \"13253df6287a46da9e58de0db31f2993\", \"artifact_path\": \"model\", \"utc_time_created\": \"2024-04-06 19:01:41.342489\", \"flavors\": {\"python_function\": {\"model_path\": \"model.pkl\", \"predict_fn\": \"predict\", \"loader_module\": \"mlflow.sklearn\", \"python_version\": \"3.9.16\", \"env\": {\"conda\": \"conda.yaml\", \"virtualenv\": \"python_env.yaml\"}}, \"sklearn\": {\"pickled_model\": \"model.pkl\", \"sklearn_version\": \"1.2.2\", \"serialization_format\": \"cloudpickle\", \"code\": null}}, \"model_uuid\": \"2bff04d096e34e0895b555aadafee967\", \"mlflow_version\": \"2.3.0\"}]','13253df6287a46da9e58de0db31f2993'),('mlflow.log-model.history','[{\"run_id\": \"2377c988458446db8be230afca1cbea3\", \"artifact_path\": \"model\", \"utc_time_created\": \"2024-04-08 01:48:07.725176\", \"flavors\": {\"python_function\": {\"model_path\": \"model.pkl\", \"predict_fn\": \"predict\", \"loader_module\": \"mlflow.sklearn\", \"python_version\": \"3.9.16\", \"env\": {\"conda\": \"conda.yaml\", \"virtualenv\": \"python_env.yaml\"}}, \"sklearn\": {\"pickled_model\": \"model.pkl\", \"sklearn_version\": \"1.2.2\", \"serialization_format\": \"cloudpickle\", \"code\": null}}, \"model_uuid\": \"3ebafb3dab6044a4bf0faa8e3963aff3\", \"mlflow_version\": \"2.3.0\"}]','2377c988458446db8be230afca1cbea3'),('mlflow.log-model.history','[{\"run_id\": \"34e74b048bc74981b6ebfddc62524461\", \"artifact_path\": \"model\", \"utc_time_created\": \"2024-04-05 03:54:38.417251\", \"flavors\": {\"python_function\": {\"model_path\": \"model.pkl\", \"predict_fn\": \"predict\", \"loader_module\": \"mlflow.sklearn\", \"python_version\": \"3.9.16\", \"env\": {\"conda\": \"conda.yaml\", \"virtualenv\": \"python_env.yaml\"}}, \"sklearn\": {\"pickled_model\": \"model.pkl\", \"sklearn_version\": \"1.2.2\", \"serialization_format\": \"cloudpickle\", \"code\": null}}, \"model_uuid\": \"936f81c005584c7e84c0235a19d5f0c4\", \"mlflow_version\": \"2.3.0\"}]','34e74b048bc74981b6ebfddc62524461'),('mlflow.log-model.history','[{\"run_id\": \"3ab0948239c74a78bf8d82176fa4f996\", \"artifact_path\": \"model\", \"utc_time_created\": \"2024-04-06 02:49:38.872849\", \"flavors\": {\"python_function\": {\"model_path\": \"model.pkl\", \"predict_fn\": \"predict\", \"loader_module\": \"mlflow.sklearn\", \"python_version\": \"3.9.16\", \"env\": {\"conda\": \"conda.yaml\", \"virtualenv\": \"python_env.yaml\"}}, \"sklearn\": {\"pickled_model\": \"model.pkl\", \"sklearn_version\": \"1.2.2\", \"serialization_format\": \"cloudpickle\", \"code\": null}}, \"model_uuid\": \"78102befa08a4adca56132228a9024a7\", \"mlflow_version\": \"2.3.0\"}]','3ab0948239c74a78bf8d82176fa4f996'),('mlflow.log-model.history','[{\"run_id\": \"4cb5283913974b72895d53e0c230989e\", \"artifact_path\": \"model\", \"utc_time_created\": \"2024-04-06 16:36:11.088822\", \"flavors\": {\"python_function\": {\"model_path\": \"model.pkl\", \"predict_fn\": \"predict\", \"loader_module\": \"mlflow.sklearn\", \"python_version\": \"3.9.16\", \"env\": {\"conda\": \"conda.yaml\", \"virtualenv\": \"python_env.yaml\"}}, \"sklearn\": {\"pickled_model\": \"model.pkl\", \"sklearn_version\": \"1.2.2\", \"serialization_format\": \"cloudpickle\", \"code\": null}}, \"model_uuid\": \"96a668e4dcf046a69f7d2dada8ca7d17\", \"mlflow_version\": \"2.3.0\"}]','4cb5283913974b72895d53e0c230989e'),('mlflow.log-model.history','[{\"run_id\": \"5242254aee3c4c48917a198e012b145c\", \"artifact_path\": \"model\", \"utc_time_created\": \"2024-04-06 19:15:25.442212\", \"flavors\": {\"python_function\": {\"model_path\": \"model.pkl\", \"predict_fn\": \"predict\", \"loader_module\": \"mlflow.sklearn\", \"python_version\": \"3.9.16\", \"env\": {\"conda\": \"conda.yaml\", \"virtualenv\": \"python_env.yaml\"}}, \"sklearn\": {\"pickled_model\": \"model.pkl\", \"sklearn_version\": \"1.2.2\", \"serialization_format\": \"cloudpickle\", \"code\": null}}, \"model_uuid\": \"2fb035399c97433d9fa75843b8f2295a\", \"mlflow_version\": \"2.3.0\"}]','5242254aee3c4c48917a198e012b145c'),('mlflow.log-model.history','[{\"run_id\": \"60c7bc3ddcc84815adf8ccbe68b1f0be\", \"artifact_path\": \"model\", \"utc_time_created\": \"2024-04-06 04:15:19.708786\", \"flavors\": {\"python_function\": {\"model_path\": \"model.pkl\", \"predict_fn\": \"predict\", \"loader_module\": \"mlflow.sklearn\", \"python_version\": \"3.9.16\", \"env\": {\"conda\": \"conda.yaml\", \"virtualenv\": \"python_env.yaml\"}}, \"sklearn\": {\"pickled_model\": \"model.pkl\", \"sklearn_version\": \"1.2.2\", \"serialization_format\": \"cloudpickle\", \"code\": null}}, \"model_uuid\": \"a3fd225eb7d8425cbab30dc77c8758b6\", \"mlflow_version\": \"2.3.0\"}]','60c7bc3ddcc84815adf8ccbe68b1f0be'),('mlflow.log-model.history','[{\"run_id\": \"61bf01c99c3e43c7ad62dddb0d6f79d5\", \"artifact_path\": \"model\", \"utc_time_created\": \"2024-04-06 02:03:10.165810\", \"flavors\": {\"python_function\": {\"model_path\": \"model.pkl\", \"predict_fn\": \"predict\", \"loader_module\": \"mlflow.sklearn\", \"python_version\": \"3.9.16\", \"env\": {\"conda\": \"conda.yaml\", \"virtualenv\": \"python_env.yaml\"}}, \"sklearn\": {\"pickled_model\": \"model.pkl\", \"sklearn_version\": \"1.2.2\", \"serialization_format\": \"cloudpickle\", \"code\": null}}, \"model_uuid\": \"57e369be72a54afab15f4cf0587f67d8\", \"mlflow_version\": \"2.3.0\"}]','61bf01c99c3e43c7ad62dddb0d6f79d5'),('mlflow.log-model.history','[{\"run_id\": \"7062f65b8103479392c092efaaa4ad15\", \"artifact_path\": \"model\", \"utc_time_created\": \"2024-04-08 01:48:08.238222\", \"flavors\": {\"python_function\": {\"model_path\": \"model.pkl\", \"predict_fn\": \"predict\", \"loader_module\": \"mlflow.sklearn\", \"python_version\": \"3.9.16\", \"env\": {\"conda\": \"conda.yaml\", \"virtualenv\": \"python_env.yaml\"}}, \"sklearn\": {\"pickled_model\": \"model.pkl\", \"sklearn_version\": \"1.2.2\", \"serialization_format\": \"cloudpickle\", \"code\": null}}, \"model_uuid\": \"837a29ecfbb74c259354d4043922615a\", \"mlflow_version\": \"2.3.0\"}]','7062f65b8103479392c092efaaa4ad15'),('mlflow.log-model.history','[{\"run_id\": \"75ceaeca37c64a16b6728e6ca37fc105\", \"artifact_path\": \"model\", \"utc_time_created\": \"2024-04-06 02:40:08.076298\", \"flavors\": {\"python_function\": {\"model_path\": \"model.pkl\", \"predict_fn\": \"predict\", \"loader_module\": \"mlflow.sklearn\", \"python_version\": \"3.9.16\", \"env\": {\"conda\": \"conda.yaml\", \"virtualenv\": \"python_env.yaml\"}}, \"sklearn\": {\"pickled_model\": \"model.pkl\", \"sklearn_version\": \"1.2.2\", \"serialization_format\": \"cloudpickle\", \"code\": null}}, \"model_uuid\": \"a609bbba5b454c238cb2a5926d1f9ef3\", \"mlflow_version\": \"2.3.0\"}]','75ceaeca37c64a16b6728e6ca37fc105'),('mlflow.log-model.history','[{\"run_id\": \"75dcda9566ba44a682adec6514139fb5\", \"artifact_path\": \"model\", \"utc_time_created\": \"2024-04-05 03:58:31.340575\", \"flavors\": {\"python_function\": {\"model_path\": \"model.pkl\", \"predict_fn\": \"predict\", \"loader_module\": \"mlflow.sklearn\", \"python_version\": \"3.9.16\", \"env\": {\"conda\": \"conda.yaml\", \"virtualenv\": \"python_env.yaml\"}}, \"sklearn\": {\"pickled_model\": \"model.pkl\", \"sklearn_version\": \"1.2.2\", \"serialization_format\": \"cloudpickle\", \"code\": null}}, \"model_uuid\": \"3446864c7e6d4779ac8e2e5dd7b60621\", \"mlflow_version\": \"2.3.0\"}]','75dcda9566ba44a682adec6514139fb5'),('mlflow.log-model.history','[{\"run_id\": \"8a3ff5c275e74facbf12a73efcc759fe\", \"artifact_path\": \"model\", \"utc_time_created\": \"2024-04-06 17:28:59.123946\", \"flavors\": {\"python_function\": {\"model_path\": \"model.pkl\", \"predict_fn\": \"predict\", \"loader_module\": \"mlflow.sklearn\", \"python_version\": \"3.9.16\", \"env\": {\"conda\": \"conda.yaml\", \"virtualenv\": \"python_env.yaml\"}}, \"sklearn\": {\"pickled_model\": \"model.pkl\", \"sklearn_version\": \"1.2.2\", \"serialization_format\": \"cloudpickle\", \"code\": null}}, \"model_uuid\": \"6bdf397748bb4315ba9e407d9b80e23d\", \"mlflow_version\": \"2.3.0\"}]','8a3ff5c275e74facbf12a73efcc759fe'),('mlflow.log-model.history','[{\"run_id\": \"9b13d777c0a34fda8751552723a20bf6\", \"artifact_path\": \"model\", \"utc_time_created\": \"2024-04-05 04:13:06.834033\", \"flavors\": {\"python_function\": {\"model_path\": \"model.pkl\", \"predict_fn\": \"predict\", \"loader_module\": \"mlflow.sklearn\", \"python_version\": \"3.9.16\", \"env\": {\"conda\": \"conda.yaml\", \"virtualenv\": \"python_env.yaml\"}}, \"sklearn\": {\"pickled_model\": \"model.pkl\", \"sklearn_version\": \"1.2.2\", \"serialization_format\": \"cloudpickle\", \"code\": null}}, \"model_uuid\": \"a6683a0932d44acea27ae36b49a67b6c\", \"mlflow_version\": \"2.3.0\"}]','9b13d777c0a34fda8751552723a20bf6'),('mlflow.log-model.history','[{\"run_id\": \"adeb210dde6e4e27a254c20ffdfcb7da\", \"artifact_path\": \"model\", \"utc_time_created\": \"2024-04-06 19:01:38.279330\", \"flavors\": {\"python_function\": {\"model_path\": \"model.pkl\", \"predict_fn\": \"predict\", \"loader_module\": \"mlflow.sklearn\", \"python_version\": \"3.9.16\", \"env\": {\"conda\": \"conda.yaml\", \"virtualenv\": \"python_env.yaml\"}}, \"sklearn\": {\"pickled_model\": \"model.pkl\", \"sklearn_version\": \"1.2.2\", \"serialization_format\": \"cloudpickle\", \"code\": null}}, \"model_uuid\": \"f7e4f934e3164a9999407b207be6649f\", \"mlflow_version\": \"2.3.0\"}]','adeb210dde6e4e27a254c20ffdfcb7da'),('mlflow.log-model.history','[{\"run_id\": \"f77cf7308e80493b94398a85be68a209\", \"artifact_path\": \"model\", \"utc_time_created\": \"2024-04-06 04:24:57.096163\", \"flavors\": {\"python_function\": {\"model_path\": \"model.pkl\", \"predict_fn\": \"predict\", \"loader_module\": \"mlflow.sklearn\", \"python_version\": \"3.9.16\", \"env\": {\"conda\": \"conda.yaml\", \"virtualenv\": \"python_env.yaml\"}}, \"sklearn\": {\"pickled_model\": \"model.pkl\", \"sklearn_version\": \"1.2.2\", \"serialization_format\": \"cloudpickle\", \"code\": null}}, \"model_uuid\": \"31d72473ba07492f898f124b56fe8ed1\", \"mlflow_version\": \"2.3.0\"}]','f77cf7308e80493b94398a85be68a209'),('mlflow.log-model.history','[{\"run_id\": \"ff3c7b58f2774afab7b7e3c389a3b710\", \"artifact_path\": \"model\", \"utc_time_created\": \"2024-04-06 02:20:03.296401\", \"flavors\": {\"python_function\": {\"model_path\": \"model.pkl\", \"predict_fn\": \"predict\", \"loader_module\": \"mlflow.sklearn\", \"python_version\": \"3.9.16\", \"env\": {\"conda\": \"conda.yaml\", \"virtualenv\": \"python_env.yaml\"}}, \"sklearn\": {\"pickled_model\": \"model.pkl\", \"sklearn_version\": \"1.2.2\", \"serialization_format\": \"cloudpickle\", \"code\": null}}, \"model_uuid\": \"e59fdf268e304521b2030e88745da99b\", \"mlflow_version\": \"2.3.0\"}]','ff3c7b58f2774afab7b7e3c389a3b710'),('mlflow.runName','cover_type_class','13253df6287a46da9e58de0db31f2993'),('mlflow.runName','test_1','1c858e176dff4d72acc0787fee7b5b1d'),('mlflow.runName','cover_type_class','2377c988458446db8be230afca1cbea3'),('mlflow.runName','test_1','269d3b734c14417db8df169fd8b1440f'),('mlflow.runName','test_1','34e74b048bc74981b6ebfddc62524461'),('mlflow.runName','cover_type_class','3ab0948239c74a78bf8d82176fa4f996'),('mlflow.runName','cover_type_class','4cb5283913974b72895d53e0c230989e'),('mlflow.runName','cover_type_class','5242254aee3c4c48917a198e012b145c'),('mlflow.runName','cover_type_class','60c7bc3ddcc84815adf8ccbe68b1f0be'),('mlflow.runName','test_1','61bf01c99c3e43c7ad62dddb0d6f79d5'),('mlflow.runName','cover_type_class','7062f65b8103479392c092efaaa4ad15'),('mlflow.runName','cover_type_class','75ceaeca37c64a16b6728e6ca37fc105'),('mlflow.runName','test_1','75dcda9566ba44a682adec6514139fb5'),('mlflow.runName','cover_type_class','8a3ff5c275e74facbf12a73efcc759fe'),('mlflow.runName','test_1','9b13d777c0a34fda8751552723a20bf6'),('mlflow.runName','cover_type_class','adeb210dde6e4e27a254c20ffdfcb7da'),('mlflow.runName','test_1','b86132597fcf49959a83fddab6b94198'),('mlflow.runName','cover_type_class','f77cf7308e80493b94398a85be68a209'),('mlflow.runName','test_1','ff3c7b58f2774afab7b7e3c389a3b710'),('mlflow.source.name','/home/airflow/.local/bin/airflow','13253df6287a46da9e58de0db31f2993'),('mlflow.source.name','/home/airflow/.local/bin/airflow','1c858e176dff4d72acc0787fee7b5b1d'),('mlflow.source.name','/home/airflow/.local/bin/airflow','2377c988458446db8be230afca1cbea3'),('mlflow.source.name','/home/airflow/.local/bin/airflow','269d3b734c14417db8df169fd8b1440f'),('mlflow.source.name','/home/airflow/.local/bin/airflow','34e74b048bc74981b6ebfddc62524461'),('mlflow.source.name','/home/airflow/.local/bin/airflow','3ab0948239c74a78bf8d82176fa4f996'),('mlflow.source.name','/home/airflow/.local/bin/airflow','4cb5283913974b72895d53e0c230989e'),('mlflow.source.name','/home/airflow/.local/bin/airflow','5242254aee3c4c48917a198e012b145c'),('mlflow.source.name','/home/airflow/.local/bin/airflow','60c7bc3ddcc84815adf8ccbe68b1f0be'),('mlflow.source.name','/home/airflow/.local/bin/airflow','61bf01c99c3e43c7ad62dddb0d6f79d5'),('mlflow.source.name','/home/airflow/.local/bin/airflow','7062f65b8103479392c092efaaa4ad15'),('mlflow.source.name','/home/airflow/.local/bin/airflow','75ceaeca37c64a16b6728e6ca37fc105'),('mlflow.source.name','/home/airflow/.local/bin/airflow','75dcda9566ba44a682adec6514139fb5'),('mlflow.source.name','/home/airflow/.local/bin/airflow','8a3ff5c275e74facbf12a73efcc759fe'),('mlflow.source.name','/home/airflow/.local/bin/airflow','9b13d777c0a34fda8751552723a20bf6'),('mlflow.source.name','/home/airflow/.local/bin/airflow','adeb210dde6e4e27a254c20ffdfcb7da'),('mlflow.source.name','/home/airflow/.local/bin/airflow','b86132597fcf49959a83fddab6b94198'),('mlflow.source.name','/home/airflow/.local/bin/airflow','f77cf7308e80493b94398a85be68a209'),('mlflow.source.name','/home/airflow/.local/bin/airflow','ff3c7b58f2774afab7b7e3c389a3b710'),('mlflow.source.type','LOCAL','13253df6287a46da9e58de0db31f2993'),('mlflow.source.type','LOCAL','1c858e176dff4d72acc0787fee7b5b1d'),('mlflow.source.type','LOCAL','2377c988458446db8be230afca1cbea3'),('mlflow.source.type','LOCAL','269d3b734c14417db8df169fd8b1440f'),('mlflow.source.type','LOCAL','34e74b048bc74981b6ebfddc62524461'),('mlflow.source.type','LOCAL','3ab0948239c74a78bf8d82176fa4f996'),('mlflow.source.type','LOCAL','4cb5283913974b72895d53e0c230989e'),('mlflow.source.type','LOCAL','5242254aee3c4c48917a198e012b145c'),('mlflow.source.type','LOCAL','60c7bc3ddcc84815adf8ccbe68b1f0be'),('mlflow.source.type','LOCAL','61bf01c99c3e43c7ad62dddb0d6f79d5'),('mlflow.source.type','LOCAL','7062f65b8103479392c092efaaa4ad15'),('mlflow.source.type','LOCAL','75ceaeca37c64a16b6728e6ca37fc105'),('mlflow.source.type','LOCAL','75dcda9566ba44a682adec6514139fb5'),('mlflow.source.type','LOCAL','8a3ff5c275e74facbf12a73efcc759fe'),('mlflow.source.type','LOCAL','9b13d777c0a34fda8751552723a20bf6'),('mlflow.source.type','LOCAL','adeb210dde6e4e27a254c20ffdfcb7da'),('mlflow.source.type','LOCAL','b86132597fcf49959a83fddab6b94198'),('mlflow.source.type','LOCAL','f77cf7308e80493b94398a85be68a209'),('mlflow.source.type','LOCAL','ff3c7b58f2774afab7b7e3c389a3b710'),('mlflow.user','root','13253df6287a46da9e58de0db31f2993'),('mlflow.user','root','1c858e176dff4d72acc0787fee7b5b1d'),('mlflow.user','root','2377c988458446db8be230afca1cbea3'),('mlflow.user','root','269d3b734c14417db8df169fd8b1440f'),('mlflow.user','root','34e74b048bc74981b6ebfddc62524461'),('mlflow.user','root','3ab0948239c74a78bf8d82176fa4f996'),('mlflow.user','root','4cb5283913974b72895d53e0c230989e'),('mlflow.user','root','5242254aee3c4c48917a198e012b145c'),('mlflow.user','root','60c7bc3ddcc84815adf8ccbe68b1f0be'),('mlflow.user','root','61bf01c99c3e43c7ad62dddb0d6f79d5'),('mlflow.user','root','7062f65b8103479392c092efaaa4ad15'),('mlflow.user','root','75ceaeca37c64a16b6728e6ca37fc105'),('mlflow.user','root','75dcda9566ba44a682adec6514139fb5'),('mlflow.user','root','8a3ff5c275e74facbf12a73efcc759fe'),('mlflow.user','root','9b13d777c0a34fda8751552723a20bf6'),('mlflow.user','root','adeb210dde6e4e27a254c20ffdfcb7da'),('mlflow.user','root','b86132597fcf49959a83fddab6b94198'),('mlflow.user','root','f77cf7308e80493b94398a85be68a209'),('mlflow.user','root','ff3c7b58f2774afab7b7e3c389a3b710');
/*!40000 ALTER TABLE `tags` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'mlflow'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-04-21 17:13:54
