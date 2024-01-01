CREATE TABLE courier (
    id_courier INT PRIMARY KEY,
    courier_name VARCHAR(40),
    phone_number VARCHAR(20),
    transport VARCHAR(20)
);


CREATE TABLE pick_up_point (
    id_pick_up_point INT PRIMARY KEY,
    address VARCHAR(150),
    payment_types VARCHAR(50),
    storage_duration INT,
    working_time VARCHAR(20)
);


CREATE TABLE client (
    id_client INT PRIMARY KEY,
    client_name VARCHAR(40),
    gender VARCHAR(10),
    phone_number VARCHAR(20),
    clothes_size INT
);


CREATE TABLE orders (
    id_order INT PRIMARY KEY,
    sum FLOAT,
    discount INT,
    id_client INT,
    FOREIGN KEY (id_client) REFERENCES client(id_client)
);


CREATE TABLE shipper (
    id_shipper INT PRIMARY KEY,
    company_name VARCHAR(40)
);


CREATE TABLE storage (
    id_comment INT PRIMARY KEY,
    address VARCHAR(150),
    working_time VARCHAR(20),
    capacity INT
);


CREATE TABLE product (
    id_product INT PRIMARY KEY,
    brand VARCHAR(20),
    season VARCHAR(20),
    size INT,
    gender VARCHAR(10),
    product_type VARCHAR(20),
    color VARCHAR(20),
    material VARCHAR(20),
    price FLOAT,
    origin_country VARCHAR(20),
    id_shipper INT,
    FOREIGN KEY (id_shipper) REFERENCES shipper(id_shipper)
);


CREATE TABLE parcel (
    id_parcel INT PRIMARY KEY,
    payment_type VARCHAR(20),
    delivery_type VARCHAR(20),
    delivery_time_start DATETIME,
    delivery_time_end DATETIME,
    address VARCHAR(150),
    id_courier INT,
    id_storage INT,
    id_order INT,
    FOREIGN KEY (id_courier) REFERENCES courier(id_courier),
    FOREIGN KEY (id_storage) REFERENCES storage(id_storage),
    FOREIGN KEY (id_order) REFERENCES orders(id_order)
);



CREATE TABLE client_pick_up_point (
    id_client INT,
    id_pick_up_point INT,
    FOREIGN KEY (id_client) REFERENCES client(id_client),
    FOREIGN KEY (id_pick_up_point) REFERENCES pick_up_point(id_pick_up_point),
    CONSTRAINT PK_client_pick_up_point PRIMARY KEY (id_client, id_pick_up_point)
);


CREATE TABLE courier_pick_up_point (
    id_courier INT,
    id_pick_up_point INT,
    FOREIGN KEY (id_courier) REFERENCES courier(id_courier),
    FOREIGN KEY (id_pick_up_point) REFERENCES pick_up_point(id_pick_up_point),
    CONSTRAINT PK_courier_pick_up_point PRIMARY KEY (id_courier, id_pick_up_point)
);


CREATE TABLE product_order (
    id_product INT,
    id_order INT,
    quantity INT,
    FOREIGN KEY (id_product) REFERENCES product(id_product),
    FOREIGN KEY (id_order) REFERENCES orders(id_order),
    CONSTRAINT PK_product_order PRIMARY KEY (id_product, id_order)
);


CREATE TABLE product_storage (
    id_product INT,
    id_storage INT,
    quantity INT,
    FOREIGN KEY (id_product) REFERENCES product(id_product),
    FOREIGN KEY (id_storage) REFERENCES storage(id_storage),
    CONSTRAINT PK_product_storage PRIMARY KEY (id_product, id_storage)
);
