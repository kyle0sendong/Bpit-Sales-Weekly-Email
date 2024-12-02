def create_lookup_sales_customer_table(connection):
    try:
        cursor = connection.cursor()
        table_name = 'Lookup_Sales_Customer'
        if cursor.tables(table=table_name).fetchone():
            print(f"{table_name} table already exist")
        else:
            print(f"Creating {table_name} table")
            cursor.execute(
                f"CREATE TABLE {table_name}("
                f"Id INT PRIMARY KEY AUTO_INCREMENT, "
                f"CustomerId int(5) NOT NULL, "
                f"SalesId int(5) NOT NULL"
                f");"
            )

            cursor.execute(
                f"ALTER TABLE {table_name} "
                f"ADD FOREIGN KEY (CustomerId) "
                f"REFERENCES Customer(Id) "
                f"ON DELETE CASCADE ON UPDATE CASCADE;"
            )

            cursor.execute(
                f"ALTER TABLE {table_name} "
                f"ADD FOREIGN KEY (SalesId) "
                f"REFERENCES Sales(Id) "
                f"ON DELETE CASCADE ON UPDATE CASCADE;"
            )

            cursor.close()
            connection.close()
    except Exception as e:
        print(e)
        return
