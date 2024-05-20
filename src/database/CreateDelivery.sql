DROP DATABASE IF EXISTS deliverydb;

CREATE DATABASE IF NOT EXISTS deliverydb;

USE deliverydb;

CREATE TABLE validStatus(
    statusId varchar(15) primary key not null,
    statusDescription varchar(255) not null
) ENGINE=INNODB;


INSERT INTO validStatus(statusiD, statusDescription) VALUES
    ("STATUS-01", "Pedido confirmado"),
    ("STATUS-02", "Pedido enviado"),
    ("STATUS-03", "Entrega confirmada"),
    ("STATUS-04", "Entrega cancelada"),
    ("STATUS-05", "Entrega pendiente")
;


CREATE TABLE delivery(
    orderKey varchar(15) primary key not null,
    orderDate datetime,
    orderTotalQty int,
    orderUser varchar(15),
    orderAddress varchar(255),
    orderStatus varchar(15)
) ENGINE=INNODB;

DELIMITER //
    CREATE PROCEDURE addDeliveryWithUser(IN newId varchar(15), IN newDate datetime, IN newTotal int, IN newUser varchar(100), IN newAddress varchar(255))
    BEGIN
        INSERT INTO delivery (orderKey, orderDate, orderTotalQty, orderUser, orderAddress, orderStatus) VALUES (newId, newDate, newTotal, newUser, newAddress, "STATUS-01");
    END //

    CREATE PROCEDURE addDeliveryNoUser(IN newId varchar(15), IN newDate datetime, IN newTotal int, IN newAddress varchar(255))
    BEGIN
        INSERT INTO delivery (orderKey, orderDate, orderTotalQty, orderAddress, orderStatus) VALUES (newId, newDate, newTotal, newAddress, "STATUS-01");
    END //

DELIMITER ;