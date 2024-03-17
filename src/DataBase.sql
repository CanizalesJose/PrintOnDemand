DROP DATABASE IF EXISTS printOnDemand;

CREATE DATABASE IF NOT EXISTS printOnDemand;

USE printOnDemand;

CREATE TABLE IF NOT EXISTS userTypes(
    typeId tinyInt primary key not null, 
    userTypeName varchar(50) not null
);

CREATE TABLE IF NOT EXISTS users(
    userName varchar(100) primary key not null,
    userType tinyInt,
    userPassword varchar(120) not null,
    foreign key (userType) references userTypes(typeId)
    on delete cascade
) ENGINE=INNODB;

CREATE TABLE IF NOT EXISTS orders(
    orderId varchar(15) primary key not null,
    orderDate datetime,
    orderTotalCost float,
    orderUser varchar(15) null,
    orderAddress varchar(255),
    foreign key (orderUser) references users(userName) on delete set null on update cascade
) ENGINE=INNODB;

-- modelFile es el nombre del archivo, vamos a imaginar que se sube el modelo
CREATE TABLE IF NOT EXISTS models3D(
    modelId varchar(15) primary key not null,
    modelName varchar (255),
    modelImage varchar(255),
    modelFile varchar(255),
    modelBasePrice float
) ENGINE=INNODB;

CREATE TABLE IF NOT EXISTS materials(
    materialId varchar(15) primary key not null,
    materialName varchar(255),
    materialPriceModifier float
) ENGINE=INNODB;

CREATE TABLE IF NOT EXISTS validMaterials(
    validMaterialsId int AUTO_INCREMENT primary key,
    modelKey varchar(15) not null,
    materialKey varchar(15) not null,
    unique key (modelKey, materialKey),
    foreign key (modelKey) references models3D(modelId)
    on delete cascade,
    foreign key (materialKey) references materials(materialId)
    on delete cascade
)ENGINE=INNODB;

CREATE TABLE IF NOT EXISTS orderMaterials(
    orderKey varchar(15) not null,
    modelKey varchar(15) not null,
    materialKey varchar(15) not null,
    modelQuantity int,
    primary key (orderKey, modelKey, materialKey),
    foreign key (modelKey, materialKey) references validMaterials(modelKey, materialKey)
    on delete no action
) ENGINE=INNODB;

-- Creación de procedimientos

DELIMITER //
    CREATE PROCEDURE iniciarSesion(IN inputUsername varchar(100), IN inputUserPassword varchar(120))
    BEGIN
        DECLARE storedPassword varchar(255);
        SELECT userPassword INTO storedPassword FROM users WHERE username = inputUsername;

        IF storedPassword IS NOT NULL AND storedPassword = SHA2(inputUserPassword, 256) THEN
            SELECT userName, userType, userPassword FROM users WHERE userName=inputUsername;
        ELSE
            SELECT NULL;
        END IF;
    END //

    CREATE PROCEDURE registrarUser(IN inputUserName varchar(100), IN inputUserPassword varchar(120), IN inputUserType tinyInt)
    BEGIN

        DECLARE hashedPassword varchar(255);
        SET hashedPassword = SHA2(inputUserPassword, 256);
        INSERT INTO users (userName, userPassword, userType) 
        VALUES (inputUserName, hashedPassword, inputUserType);
        

    END //

    CREATE PROCEDURE getAllModels()
    BEGIN
        SELECT modelId, modelName, modelImage, modelFile, modelBasePrice from models3D;
    END //
    
    CREATE PROCEDURE registrarMaterial(IN inputMaterialId VARCHAR(15), IN inputMaterialName VARCHAR(255), IN inputMaterialPriceModifier FLOAT)
    BEGIN
		INSERT INTO materials (materialId, materialName, materialPriceModifier) VALUES (inputMaterialId, inputMaterialName, inputMaterialPriceModifier);
    END //
    
    CREATE PROCEDURE registrarValidMaterial(IN inputModelKey varchar(15), IN inputMaterialKey varchar(15))
    BEGIN
		INSERT INTO validmaterials (modelKey, materialKey) VALUES (inputModelKey, inputMaterialKey);
    END //
    
    CREATE PROCEDURE registrarModelo(IN inputModelId varchar(15), IN inputModelName varchar(255), IN inputModelImage varchar(255), IN inputModelFile varchar(255), IN inputModelBasePrice float)
    BEGIN
		INSERT INTO models3d (modelId, modelName, modelImage, modelFile, modelBasePrice) VALUES (inputModelId, inputModelName, inputModelImage, inputModelFile, inputModelBasePrice);
    END //
    
    CREATE PROCEDURE showAllModelId()
    BEGIN
		select modelId from models3D;
    END //
    
    CREATE PROCEDURE showCatalogData(IN inputModelId varchar(15))
    BEGIN
		SELECT modelId, modelName, modelImage, modelFile, modelBasePrice from validmaterials 
        INNER JOIN models3d ON validMaterials.modelKey = models3d.modelId 
        WHERE modelId = inputModelId
        GROUP BY modelId;
    END //
    
    CREATE PROCEDURE getMaterialsFromModel(IN inputModelId varchar(15))
    BEGIN
		SELECT materialId, materialName, materialPriceModifier from validMaterials
        INNER JOIN materials ON validMaterials.materialKey = materials.materialId
        WHERE modelKey = inputModelId
        GROUP BY materialId;
    END //
    
	CREATE PROCEDURE deleteModel3D(IN inputModelId varchar(15))
    BEGIN
		delete from models3d where modelId = inputModelId;
    END //
    
    CREATE PROCEDURE deleteMaterial(IN inputMaterialId varchar(15))
    BEGIN
		delete from materials where materialId = inputMaterialId;
    END //
    
    CREATE PROCEDURE deleteValidMaterial(IN inputModelKey varchar(15), IN inputMaterialKey varchar(15))
    BEGIN
		delete from validmaterials where modelKey = inputModelKey and materialKey = inputMaterialKey;
    END //
    
    CREATE PROCEDURE updateUser(IN currentUsername varchar(100), IN inputUsername varchar(100), in inputUserType tinyint)
    BEGIN
		update users set userName = inputUsername, userType = inputUserType where userName = currentUsername;
    END //
    
    CREATE PROCEDURE deleteUser(IN deletedUsername varchar(100))
    BEGIN
		delete from users where userName = deletedUsername;
    END //
DELIMITER ;