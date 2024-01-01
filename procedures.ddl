IF OBJECT_ID('GetClientPurchases', 'P') IS NOT NULL
    DROP PROC GetClientPurchases;

GO

CREATE PROCEDURE GetClientPurchases @id_client INT
AS 
BEGIN
    SELECT order.id_order, product.id_product, product.product_type, product.price
    FROM order
        JOIN product_order ON order.id_order = product_order.id_order
        JOIN product ON product_order.id_product = product.id_product
    WHERE order.id_client = @id_client
END;
GO


IF OBJECT_ID('GetCourierTimetable', 'P') IS NOT NULL
    DROP PROC GetCourierTimetable;

GO

CREATE PROCEDURE GetCourierTimetable @id_courier INT, @delivery_time_start DATETIME, @delivery_time_end DATETIME
AS 
BEGIN
    SELECT parcel.delivery_time_start, parcel.delivery_time_end, parcel.id_parcel, parcel.delivery_type, parcel.address, client.client_name
    FROM parcel
        JOIN order ON parcel.id_order = order.id_order
        JOIN client ON order.id_client = client.id_client
    WHERE parcel.id_courier = @id_courier AND parcel.delivery_time_start < @delivery_time_end
                                          AND parcel.delivery_time_end > @delivery_time_start
    ORDER BY parcel.delivery_time_start
END;
GO


IF OBJECT_ID('GetOrderSummary', 'P') IS NOT NULL
    DROP PROC GetOrderSummary;

GO

CREATE PROCEDURE GetOrderSummary @id_order INT
AS 
BEGIN
    SELECT order.id_order, order.sum, order.discount, client.id_client, client.name, client.phone_number
    FROM order
        JOIN client ON order.id_client = client.id_client
    WHERE order.id_order = @id_order
END;
GO


IF OBJECT_ID('GetOrderParcels', 'P') IS NOT NULL
    DROP PROC GetOrderParcels;

GO

CREATE PROCEDURE GetOrderParcels @id_order INT
AS 
BEGIN
    SELECT id_parcel, payment_type, delivery_type, delivery_time_start, delivery_time_end, address, id_courier, id_storage
    FROM parcel
    WHERE parcel.id_order = @id_order
END;
GO


CREATE TABLE History_Products (
    id_operation INT PRIMARY KEY,
    id_product INT,
    operation VARCHAR(200),
    operation_time DATETIME DEFAULT GETDATE(),
);
GO

CREATE TRIGGER Product_INSERT ON product
AFTER INSERT
AS
BEGIN
    INSERT INTO History_Products(id_product, operation)
    SELECT id_operation, 'Добавлен товар ' + product.product_type + 'бренда' + product.brand
    FROM INSERTED
END;
GO

CREATE TRIGGER Product_DELETE ON product
AFTER DELETE
AS
BEGIN
    INSERT INTO History_Products(id_product, operation)
    SELECT id_operation, 'Удален товар ' + product.product_type + 'бренда' + product.brand
    FROM DELETED
END;
