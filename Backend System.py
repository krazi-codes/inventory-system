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
    #_______________THIS IS TYLER SQL CODE
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

def view_inventory():
    conn = InventoryManager.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM inventory")
    result = cursor.fetchall()
    
    print("\n--- Current Inventory ---")
    print(f"{'ID':<10} {'Name':<20} {'Qty':<10} {'Price':<10}")
    print("-" * 50)
    for row in result:
        # row indexes: 0=ID, 1=Name, 2=Qty, 3=Price
        print(f"{row[0]:<10} {row[1]:<20} {row[2]:<10} ${row[3]:<10}")
    print("-" * 50 + "\n")
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

#-----------------BELOW IS ISSAM CODE
    def get_product_id(self):
        
        return self.product_id
        

    def get_name(self):
        return self.name

    def get_price(self):
        return self.price

    def search_product(products, product_id):
        for product in products:
            if product.get_product_id() == product_id:
                return product
        return None
        
class Customer:
    def __init__(self, customer_id, name, email):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        logging.info(f"Instantiated Customer Object: {self.customer_id} {self.name} {self.email}")

    def get_customer_id(self):
        return self.customer_id

    def get_name(self):
        return self.name

    def get_email(self):
        return self.email

    def search_customer(customers, customer_id):
        for customer in customers:
            if customer.get_customer_id() == customer_id:
                return customer
        return None

class Order:
    def __init__(self, order_id, customer, product, quantity):
        self.order_id = order_id
        self.customer = customer
        self.product = product
        self.quantity = quantity
        logging.info(f"Instantiated Order object {self.order_id} {self.customer} {self.product} {self.quantity}")

    def get_order_id(self):
        return self.order_id

    def calculate_total(self):
        return self.product.get_price() * self.quantity
    
    def display_order(order):
        return f"Order ID: {order.get_order_id()}, Customer: {order.customer.get_name()}, Total: {order.calculate_total()}"

class Employee:
    
    def __init__(self, employee_id, name, position):
        self.employee_id = employee_id
        self.name = name
        self.position = position
        logging.info(f"Instantiated Employee object {self.employee_id}, {self.name}, {self.position}")

    def get_employee_id(self):
        return self.employee_id

    def get_name(self):
        return self.name

    def get_position(self):
        return self.position

from datetime import datetime
current_date = datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')
print(current_date)