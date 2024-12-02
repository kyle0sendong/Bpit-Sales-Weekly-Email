def create_driver_table(connection):
    try:
        cursor = connection.cursor()
        table_name = 'Driver'
        if cursor.tables(table=table_name).fetchone():
            print(f"{table_name} table already exist")
        else:
            print(f"Creating {table_name} table")
            cursor.execute(
                f"CREATE TABLE {table_name}("
                f"Id INT PRIMARY KEY AUTO_INCREMENT, "
                f"DriverName VARCHAR(64) NOT NULL"
                f");"
            )

            cursor.close()
            connection.close()
    except Exception as e:
        print(e)
        return
