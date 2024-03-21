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

CREATE TABLE IF NOT EXISTS orderModels(
    orderKey varchar(15) not null,
    orderModelKey varchar(15) not null,
    orderModelName varchar(255) not null,
    orderModelFile varchar(255) not null,
    orderModelPrice float not null,
	orderModelQty int not null,
    orderMaterialKey varchar(15) not null,
    orderMaterialName varchar(255) not null,
    orderMaterialPriceModifier float not null,
    primary key (orderKey, orderModelKey, orderMaterialKey),
    foreign key (orderModelKey, orderMaterialKey) references validMaterials(modelKey, materialKey)
    on delete no action
) ENGINE=INNODB;

-- materialName, materialPriceModifier y customPrice son campos llenados de forma automatica
CREATE TABLE IF NOT EXISTS customOrderModels(
	orderKey varchar(15) not null,
    customModelId varchar(15) not null,
    customModelName varchar(255) not null,
    customModelFile varchar(255) not null,
    customModelPrice float not null,
    customModelQty int not null,
    customMaterialKey varchar(15) not null,
    customMaterialName varchar(255) not null,
    customMaterialPriceModifier float not null,
    primary key (orderKey, customModelId, customMaterialKey),
    foreign key (customMaterialKey) references materials(materialId) on delete no action
);

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
    
    CREATE PROCEDURE insertOrderWithUser(IN newId varchar(15), IN newDate datetime, IN newTotal float, IN newUser varchar(100), IN newAddress varchar(255))
    BEGIN
		insert into orders (orderId, orderDate, orderTotalCost, orderUser, orderAddress) values (newId, newDate, newTotal, newUser, newAddress);
    END //
    
    CREATE PROCEDURE insertOrderNoUser(IN newId varchar(15), IN newDate datetime, IN newTotal float, IN newAddress varchar(255))
    BEGIN
		insert into orders (orderId, orderDate, orderTotalCost, orderAddress) values (newId, newDate, newTotal, newAddress);
    END //
    
    CREATE PROCEDURE insertModelOrder(IN newOrderKey varchar(15), IN newModelKey varchar(15), IN newModelName varchar(255), IN newModelFile varchar(255), IN newModelPrice float, IN newModelQty int, IN newMaterialKey varchar(15), IN newMaterialName varchar(255), IN newMaterialModifier float)
    BEGIN
		insert into ordermodels values (newOrderKey, newModelKey, newModelName, newModelFile, newModelPrice, newModelQty, newMaterialKey, newMaterialName, newMaterialModifier);
    END//
    
    CREATE PROCEDURE insertCustomModelOrder(IN newOrderKey varchar(15), IN newModelKey varchar(15), IN newModelName varchar(255), IN newModelFile varchar(255), IN newModelPrice float, IN newModelQty int, IN newMaterialKey varchar(15), IN newMaterialName varchar(255), IN newMaterialModifier float)
    BEGIN
		insert into customordermodels values (newOrderKey, newModelKey, newModelName, newModelFile, newModelPrice, newModelQty, newMaterialKey, newMaterialName, newMaterialModifier);
    END//
    
DELIMITER ;