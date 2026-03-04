import os
import logging
import mysql.connector
from datetime import datetime
# 1. Setup Logging
logging.basicConfig(
    filename='backend.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# 2. Database Connection Configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',         
    'password': 'password', 
    'database': 'inventory_system'
}
def get_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        logging.error(f"Database connection failed: {err}")
        return None

class Product:
    def __init__(self, product_id, name, price):
        self.product_id = product_id
        self.name = name
        self.price = price
        logging.info(f"Product object instantiated: {self.name} {self.price} {self.product_id}")
        
    def save_to_db(self):
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            query = """
            INSERT INTO inventory (ProductID, ProductName, Price, Quantity, log)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE Quantity = %s, Price = %s, log = %s
            """
            current_time = datetime.now()
            values = (
                self.product_id, self.name, self.price, self.quantity, current_time,
                self.quantity, self.price, current_time # For the update part
            )
            
            try:
                cursor.execute(query, values)
                conn.commit()
                print(f"Success: {self.name} saved to database.")
                logging.info(f"Database INSERT/UPDATE success: {self.product_id}")
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                logging.error(f"Database error: {err}")
            finally:
                cursor.close()
                conn.close()


@staticmethod
def smart_remove_by_id(product_id):
    conn = InventoryManager.get_connection()
    # Using dictionary=True makes result['Quantity'] much easier to read
    cursor = conn.cursor(dictionary=True)

    try:
        # 1. Check if the ID exists and get the current quantity
        cursor.execute("SELECT Quantity FROM inventory WHERE ProductID = %s", (product_id,))
        record = cursor.fetchone()

        # 2. IF ID is not found, do nothing and exit
        if record is None:
            logging.info(f"Remove attempted for ID {product_id}: ID not found. No action taken.")
            return 

        current_qty = record['Quantity']

        # 3. IF ID is found, perform the quantity check
        if current_qty > 1:
            # Reduce quantity by 1
            new_qty = current_qty - 1
            update_sql = "UPDATE inventory SET Quantity = %s, log = %s WHERE ProductID = %s"
            cursor.execute(update_sql, (new_qty, datetime.now(), product_id))
            logging.info(f"ID {product_id}: Decremented to {new_qty}")
        else:
            # Quantity is 1 or less, delete the row
            delete_sql = "DELETE FROM inventory WHERE ProductID = %s"
            cursor.execute(delete_sql, (product_id,))
            logging.info(f"ID {product_id}: Quantity zeroed out, row deleted.")

        # Commit the changes to the database
        conn.commit()

    except mysql.connector.Error as err:
        logging.error(f"Database error during removal: {err}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()
