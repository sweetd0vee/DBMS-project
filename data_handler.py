# -*- coding: utf-8 -*-
import sqlite3

class SQLiter:
    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def get_order_summary(self, order_id):
        with self.connection:
            return self.cursor.execute('''
                    SELECT orders.id_order, orders.sum, orders.discount, client.id_client, client.client_name, client.phone_number
                    FROM orders
                    JOIN client ON orders.id_client = client.id_client
                    WHERE orders.id_order = ?
                   ''', (order_id, )).fetchall()

    def get_client_purchases(self, client_id):
        with self.connection:
            return self.cursor.execute('''
                SELECT orders.id_order, product.id_product, product.product_type, product.price, product_order.quantity
                FROM orders
                JOIN product_order ON orders.id_order = product_order.id_order
                JOIN product ON product_order.id_product = product.id_product
                WHERE orders.id_client = ?
            ''', (client_id, )).fetchall()

    def get_courier_timetable(self, courier_id, delivery_time_start, delivery_time_end):
        with self.connection:
            return self.cursor.execute('''
                SELECT parcel.delivery_time_start, parcel.delivery_time_end, parcel.id_parcel, parcel.delivery_type, parcel.address, client.client_name
                FROM parcel
                JOIN orders ON parcel.id_order = orders.id_order
                JOIN client ON orders.id_client = client.id_client
                WHERE parcel.id_courier = ? AND parcel.delivery_time_end > ?
                                          AND parcel.delivery_time_start < ?
                ORDER BY parcel.delivery_time_start
            ''', (courier_id, delivery_time_start, delivery_time_end)).fetchall()

    # d = [product_id, brand, season, size, gender, product_type, color, material, price, origin_country, id_shipper]
    def add_product(self, d):
        with self.connection:
            flag = self.cursor.execute('''
                    SELECT id_product
                    FROM product
                    WHERE id_product = ?
                    ''', (d[0],)).fetchall()

            if len(flag) != 0:
                return 0

        with self.connection:
            self.cursor.execute(''' 
                                    INSERT INTO product VALUES
                                    (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                                ''', (d[0], d[1], d[2], d[3], d[4], d[5], d[6], d[7], d[8], d[9], d[10], )).fetchall()
            return 1

    def get_product_info(self, product_id):
        with self.connection:
            return self.cursor.execute('''
                SELECT id_product, product_type
                FROM product
                WHERE product.id_product = ?
            ''', (product_id, )).fetchall()


    def change_address(self, order_id, address):
        with self.connection:
            flag = self.cursor.execute('''
                    SELECT id_order
                    FROM orders
                    WHERE id_order = ?
                    ''', (order_id,)).fetchall()

            if len(flag) == 0:
                return 0

        with self.connection:
            flag = self.cursor.execute('''
                    SELECT id_pick_up_point
                    FROM pick_up_point
                    WHERE address = ?
                    ''', (address,)).fetchall()
            flag1 = self.cursor.execute('''
                    SELECT delivery_type
                    FROM parcel
                    WHERE id_order = ?
                    ''', (order_id,)).fetchall()

            if (len(flag) == 0) and (flag1[0][0] == 'пункт выдачи'):
                return 1

        with self.connection:
            flag = self.cursor.execute('''
                    UPDATE parcel SET address = ?
                    WHERE id_order = ? 
                    ''', (address, order_id,)).fetchall()

            return 2

    def change_payment(self, order_id, payment):
        with self.connection:
            flag = self.cursor.execute('''
                    SELECT id_order
                    FROM orders
                    WHERE id_order = ?
                    ''', (order_id,)).fetchall()

            if len(flag) == 0:
                return 0

        with self.connection:
            self.cursor.execute('''
                    UPDATE parcel SET payment_type = ?
                    WHERE id_order = ? 
                    ''', (payment, order_id,)).fetchall()

            return 1

    def get_parcels(self, order_id):
        with self.connection:
            return self.cursor.execute('''
                            SELECT id_order, id_parcel, payment_type
                            FROM parcel
                            WHERE id_order = ? 
                            ''', (order_id,)).fetchall()

    def get_address(self, order_id):
        with self.connection:
            return self.cursor.execute('''
                            SELECT id_order, id_parcel, address
                            FROM parcel
                            WHERE id_order = ? 
                            ''', (order_id,)).fetchall()

    def close(self):
        self.connection.close()
