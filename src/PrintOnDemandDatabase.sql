CREATE DATABASE  IF NOT EXISTS `printondemand` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `printondemand`;
-- MySQL dump 10.13  Distrib 8.0.30, for Win64 (x86_64)
--
-- Host: localhost    Database: printondemand
-- ------------------------------------------------------
-- Server version	8.2.0

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
-- Table structure for table `customordermodels`
--

DROP TABLE IF EXISTS `customordermodels`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customordermodels` (
  `orderKey` varchar(15) NOT NULL,
  `customModelId` varchar(15) NOT NULL,
  `customModelName` varchar(255) NOT NULL,
  `customModelFile` varchar(255) NOT NULL,
  `customModelPrice` float NOT NULL,
  `customModelQty` int NOT NULL,
  `customMaterialKey` varchar(15) NOT NULL,
  `customMaterialName` varchar(255) NOT NULL,
  `customMaterialPriceModifier` float NOT NULL,
  PRIMARY KEY (`orderKey`,`customModelId`,`customMaterialKey`),
  KEY `customMaterialKey` (`customMaterialKey`),
  CONSTRAINT `customordermodels_ibfk_1` FOREIGN KEY (`customMaterialKey`) REFERENCES `materials` (`materialId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customordermodels`
--

LOCK TABLES `customordermodels` WRITE;
/*!40000 ALTER TABLE `customordermodels` DISABLE KEYS */;
/*!40000 ALTER TABLE `customordermodels` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `materials`
--

DROP TABLE IF EXISTS `materials`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `materials` (
  `materialId` varchar(15) NOT NULL,
  `materialName` varchar(255) DEFAULT NULL,
  `materialPriceModifier` float DEFAULT NULL,
  PRIMARY KEY (`materialId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `materials`
--

LOCK TABLES `materials` WRITE;
/*!40000 ALTER TABLE `materials` DISABLE KEYS */;
INSERT INTO `materials` VALUES ('material1','PLA',1),('material2','ABS',1.2),('material3','PETG',1.1),('material4','TPU',1.3);
/*!40000 ALTER TABLE `materials` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `models3d`
--

DROP TABLE IF EXISTS `models3d`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `models3d` (
  `modelId` varchar(15) NOT NULL,
  `modelName` varchar(255) DEFAULT NULL,
  `modelImage` varchar(255) DEFAULT NULL,
  `modelFile` varchar(255) DEFAULT NULL,
  `modelBasePrice` float DEFAULT NULL,
  PRIMARY KEY (`modelId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `models3d`
--

LOCK TABLES `models3d` WRITE;
/*!40000 ALTER TABLE `models3d` DISABLE KEYS */;
INSERT INTO `models3d` VALUES ('model1','ArticulatedWhaleShark','https://cdn.thingiverse.com/assets/d9/91/d7/44/d5/large_display_5939294b-57ab-4709-a2e5-3182f29fa89e.png','ArticulatedWhaleShark.stl',10.99),('model10','Rejilla ventilador','https://cdn.thingiverse.com/assets/67/c9/2a/2c/6c/large_display_8c03cb80-8a62-4c27-b35e-9e7d5ac9470d.png','rejilla_vent2.stl',16.9),('model2','Cabinet Door Organizer','https://cdn.thingiverse.com/assets/8a/96/8b/7a/3b/large_display_707af456-9de0-4a2c-9e8a-1e7780eeef75.png','Cabinet_Door_Organizer_5.stl',12.99),('model3','Anatomically Correct Human Skull (Homo Sapiens Sapiens)','https://cdn.thingiverse.com/assets/9a/e4/cd/5f/dc/large_display_f6557724-0b6c-4cea-bdc1-067a0a5194b9.png','Human_Skull_Cut_OBJ_3Demon.obj',8.99),('model4','8geo 3d','https://cdn.thingiverse.com/assets/fc/6c/80/e8/46/large_display_40278189-9e71-41eb-9750-6e92d2331aff.png','x8geo_3d_planter.stl',15.99),('model5','Articulated Dolphin','https://cdn.thingiverse.com/assets/b5/be/1b/af/71/large_display_89e2f9a3-7290-4152-a174-e8b640d77a84.png','Extreemly_loose_dolphin_rec.stl',9.99),('model6','Vox\'s hat','https://cdn.thingiverse.com/assets/cb/3c/26/7e/54/large_display_7675b91a-d933-479b-8cb2-4b9b0b31b4af.png','tv_hat.stl',11.99),('model7','Saturn V - Desktop Rocket','https://cdn.thingiverse.com/assets/4e/bf/63/63/42/large_display_8dc51bee-8a08-4b59-a034-71129db06b65.png','Saturn_V_Desktop_-_Rocket.stl',14.99),('model8','A-10 Warthog','https://cdn.thingiverse.com/assets/f5/71/5c/fc/64/large_display_0339506b-8ccc-429b-8ea7-64aef7bedbdc.png','A-10_Warthog.stl',13.99),('model9','Window for Dollhouse','https://cdn.thingiverse.com/assets/f4/69/fb/f5/de/large_display_0c2a8d5f-e793-43c6-ab9b-f8436656e649.png','Part_Studio_1.stl',7.99);
/*!40000 ALTER TABLE `models3d` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ordermodels`
--

DROP TABLE IF EXISTS `ordermodels`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ordermodels` (
  `orderKey` varchar(15) NOT NULL,
  `orderModelKey` varchar(15) NOT NULL,
  `orderModelName` varchar(255) NOT NULL,
  `orderModelFile` varchar(255) NOT NULL,
  `orderModelPrice` float NOT NULL,
  `orderModelQty` int NOT NULL,
  `orderMaterialKey` varchar(15) NOT NULL,
  `orderMaterialName` varchar(255) NOT NULL,
  `orderMaterialPriceModifier` float NOT NULL,
  PRIMARY KEY (`orderKey`,`orderModelKey`,`orderMaterialKey`),
  KEY `orderModelKey` (`orderModelKey`,`orderMaterialKey`),
  CONSTRAINT `ordermodels_ibfk_1` FOREIGN KEY (`orderModelKey`, `orderMaterialKey`) REFERENCES `validmaterials` (`modelKey`, `materialKey`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ordermodels`
--

LOCK TABLES `ordermodels` WRITE;
/*!40000 ALTER TABLE `ordermodels` DISABLE KEYS */;
/*!40000 ALTER TABLE `ordermodels` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders` (
  `orderId` varchar(15) NOT NULL,
  `orderDate` datetime DEFAULT NULL,
  `orderTotalCost` float DEFAULT NULL,
  `orderUser` varchar(15) DEFAULT NULL,
  `orderAddress` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`orderId`),
  KEY `orderUser` (`orderUser`),
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`orderUser`) REFERENCES `users` (`userName`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `userName` varchar(100) NOT NULL,
  `userType` tinyint DEFAULT NULL,
  `userPassword` varchar(120) NOT NULL,
  PRIMARY KEY (`userName`),
  KEY `userType` (`userType`),
  CONSTRAINT `users_ibfk_1` FOREIGN KEY (`userType`) REFERENCES `usertypes` (`typeId`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES ('admin',1,'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3'),('client',2,'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usertypes`
--

DROP TABLE IF EXISTS `usertypes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usertypes` (
  `typeId` tinyint NOT NULL,
  `userTypeName` varchar(50) NOT NULL,
  PRIMARY KEY (`typeId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usertypes`
--

LOCK TABLES `usertypes` WRITE;
/*!40000 ALTER TABLE `usertypes` DISABLE KEYS */;
INSERT INTO `usertypes` VALUES (1,'Administrador'),(2,'Usuario Cliente');
/*!40000 ALTER TABLE `usertypes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `validmaterials`
--

DROP TABLE IF EXISTS `validmaterials`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `validmaterials` (
  `validMaterialsId` int NOT NULL AUTO_INCREMENT,
  `modelKey` varchar(15) NOT NULL,
  `materialKey` varchar(15) NOT NULL,
  PRIMARY KEY (`validMaterialsId`),
  UNIQUE KEY `modelKey` (`modelKey`,`materialKey`),
  KEY `materialKey` (`materialKey`),
  CONSTRAINT `validmaterials_ibfk_1` FOREIGN KEY (`modelKey`) REFERENCES `models3d` (`modelId`) ON DELETE CASCADE,
  CONSTRAINT `validmaterials_ibfk_2` FOREIGN KEY (`materialKey`) REFERENCES `materials` (`materialId`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=118 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `validmaterials`
--

LOCK TABLES `validmaterials` WRITE;
/*!40000 ALTER TABLE `validmaterials` DISABLE KEYS */;
INSERT INTO `validmaterials` VALUES (105,'model1','material1'),(106,'model1','material2'),(107,'model1','material3'),(108,'model1','material4'),(109,'model2','material1'),(110,'model2','material2'),(111,'model2','material4'),(112,'model3','material1'),(113,'model3','material4'),(114,'model4','material1'),(115,'model4','material3'),(116,'model5','material1'),(117,'model6','material2');
/*!40000 ALTER TABLE `validmaterials` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-03-20 21:56:15
