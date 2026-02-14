import mysql.connector
from backend_system import get_db_connection, DB_CONFIG

def search_interface():
    """A standalone search bar for the terminal."""
    print("="*30)
    print(" INVENTORY SEARCH SYSTEM ")
    print("="*30)
    
    while True:
        query = input("\nEnter Product Name (or type 'exit' to quit): ").strip()
        
        if query.lower() == 'exit':
            print("Closing search tool...")
            break
        
        if not query:
            print("Please enter a search term.")
            continue

        execute_search(query)

def execute_search(search_term):
    conn = get_db_connection()
    if not conn:
        print("Error: Could not connect to database.")
        return

    try:
        cursor = conn.cursor(dictionary=True)
        sql = "SELECT ProductID, ProductName, Quantity, Price FROM inventory WHERE ProductName LIKE %s"
        cursor.execute(sql, (f"%{search_term}%",))
        
        results = cursor.fetchall()

        if results:
            print(f"\n{'ID':<10} {'Name':<20} {'Qty':<10} {'Price':<10}")
            print("-" * 50)
            for row in results:
                print(f"{row['ProductID']:<10} {row['ProductName']:<20} {row['Quantity']:<10} ${row['Price']:<10}")
        else:
            print(f"No results found for '{search_term}'.")

    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    search_interface()
