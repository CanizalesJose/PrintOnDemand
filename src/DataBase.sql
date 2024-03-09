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
) ENGINE=INNODB;

CREATE TABLE IF NOT EXISTS orders(
    orderId varchar(15) primary key not null,
    orderDate datetime,
    orderTotalCost float,
    orderUser varchar(15) null,
    orderAddress varchar(255),
    foreign key (orderUser) references users(userName)
) ENGINE=INNODB;

-- modelFile es el nombre del archivo, vamos a imaginar que se sube el modelo
CREATE TABLE IF NOT EXISTS models3D(
    modelId varchar(15) primary key,
    modelName varchar (255),
    modelImage varchar(255),
    modelFile varchar(255),
    modelBasePrice float
) ENGINE=INNODB;

CREATE TABLE IF NOT EXISTS materials(
    materialId varchar(15) primary key,
    materialName varchar(255),
    materialPriceModifier float
) ENGINE=INNODB;

CREATE TABLE IF NOT EXISTS validMaterials(
    validMaterialsId int AUTO_INCREMENT primary key,
    modelKey varchar(15),
    materialKey varchar(15),
    unique key (modelKey, materialKey),
    foreign key (modelKey) references models3D(modelId),
    foreign key (materialKey) references materials(materialId)
)ENGINE=INNODB;

CREATE TABLE IF NOT EXISTS orderMaterials(
    orderKey varchar(15),
    modelKey varchar(15),
    materialKey varchar(15),
    modelQuantity int,
    primary key (orderKey, modelKey, materialKey),
    foreign key (modelKey, materialKey) references validMaterials(modelKey, materialKey)
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

    CREATE PROCEDURE calcularPrecioModelo(IN inputModelId varchar(15))
    BEGIN
        SELECT modelName, materialName, modelBasePrice, materialPriceModifier, (modelBasePrice*materialPriceModifier) as total FROM validMaterials INNER JOIN models3D ON validMaterials.modelKey = models3D.modelId INNER JOIN materials ON validMaterials.materialKey = materials.materialId;
    END //

    CREATE PROCEDURE mostrarModelos()
    BEGIN
        SELECT modelId, modelName, modelImage, modelFile, modelBasePrice from models3D;
    END //

DELIMITER ;