import mysql.connector
# Ekhane amar Python & SQL connection.....

conn_obj = mysql.connector.connect(
    host="localhost",
    user="root",
    password="R@hul123",
    database="supermarket_db"
)
cur_obj = conn_obj.cursor()

#CURD= 'C' Create korchi ........
# Eta customer table ta ready korchi.....
def insert_customer(customer_id, customer_name, product_quantity, total_amount):
    sql = """
    INSERT INTO customers (customer_id, customer_name, product_quantity, total_amount)
    VALUES (%s, %s, %s, %s)
    """
    data = (customer_id, customer_name, product_quantity, total_amount)
    try:
        cur_obj.execute(sql, data)
        conn_obj.commit()
        print("Customer data inserted successfully.")
    except mysql.connector.Error as e:
        print("Error inserting data into MySQL:", e)
        conn_obj.rollback()

# invoice table er jonno ready krlam.......
def insert_invoice(customer_id, amount):
    sql = "INSERT INTO invoices (customer_id, amount) VALUES (%s, %s)"
    data = (customer_id, amount)
    try:
        cur_obj.execute(sql, data)
        conn_obj.commit()
        print("Invoice data inserted successfully.")
    except mysql.connector.Error as e:
        print("Error inserting invoice data:", e)
        conn_obj.rollback()

# CURD=R read korar jonno.......
def retrieve_total_spent():
    sql = """
    SELECT c.customer_name, 
           (SELECT SUM(i.amount) 
            FROM invoices i 
            WHERE i.customer_id = c.customer_id) AS total_spent
    FROM customers c;
    """
    try:
        cur_obj.execute(sql)
        results = cur_obj.fetchall()
        if results:
            print("Total amount spent by each customer:")
            for row in results:
                print(f"Customer:{row[0]}, Total Spent: {row[1]}")
        else:
            print("No data found.")
    except mysql.connector.Error as e:
        print("Error executing query:", e)

# CURD='U' update er jonno......
def update_customer(customer_id, new_name=None, new_quantity=None, new_total=None):
    updates = []
    data = []

    if new_name:
        updates.append("customer_name = %s")
        data.append(new_name)
    if new_quantity:
        updates.append("product_quantity = %s")
        data.append(new_quantity)
    if new_total:
        updates.append("total_amount = %s")
        data.append(new_total)

    if updates:
        sql = f"UPDATE customers SET {', '.join(updates)} WHERE customer_id = %s"
        data.append(customer_id)

        try:
            cur_obj.execute(sql, data)
            conn_obj.commit()
            print("Customer data updated successfully.")
        except mysql.connector.Error as e:
            print("Error updating data in MySQL:", e)
            conn_obj.rollback()
    else:
        print("No fields provided to update.")


# CURD='D' Delete hobe ;  condition= invoice r customer 2to thekei delete hobe.......
def delete_customer(customer_id):
    try:
        delete_invoices_sql = "DELETE FROM invoices WHERE customer_id = %s"
        cur_obj.execute(delete_invoices_sql,(customer_id,))
        conn_obj.commit()
        print(f"Invoices related to customer {customer_id} deleted.")


        sql = "DELETE FROM customers WHERE customer_id = %s"
        cur_obj.execute(sql, (customer_id,))
        conn_obj.commit()

        if cur_obj.rowcount > 0:
            print(f"Customer record with ID {customer_id} deleted successfully.")
        else:
            print("Customer ID not found.")
    except mysql.connector.Error as e:
        print("Error deleting data from MySQL:", e)
        conn_obj.rollback()

# Normal logic use korlam.....
def main_menu():
    while True:
        print("\nChoose an operation:")
        print("1. Insert new customer")
        print("2. Insert new invoice")
        print("3. Retrieve total amount spent by each customer")
        print("4. Update customer data")
        print("5. Delete customer data")
        print("6. Exit")
        choice = input("Enter your choice (1-6): ")

        if choice == "1":
            customer_id = int(input("Enter customer ID: "))
            customer_name = input("Enter customer name: ")
            product_quantity = int(input("Enter product quantity: "))
            total_amount = float(input("Enter total amount: "))
            insert_customer(customer_id, customer_name, product_quantity, total_amount)

        elif choice == "2":
            customer_id = int(input("Enter customer ID: "))
            amount = float(input("Enter amount for the invoice: "))
            insert_invoice(customer_id, amount)

        elif choice == "3":
            retrieve_total_spent()

        elif choice == "4":
            customer_id = int(input("Enter customer ID to update: "))
            print("Leave a field empty to keep it unchanged.")
            new_name = input("Enter new customer name: ")
            new_quantity = input("Enter new product quantity: ")
            new_total = input("Enter new total amount: ")
            update_customer(customer_id, new_name, new_quantity, new_total)

        elif choice == "5":
            customer_id = int(input("Enter customer ID to delete: "))
            delete_customer(customer_id)

        elif choice == "6":
            print("Exiting program. Goodbye!")
            break

        else:
            print("Invalid choice. Please choose between 1 and 6.")


main_menu()

conn_obj.close()
