def create_arm_table(connection):
    try:
        cursor = connection.cursor()
        table_name = 'Arm'
        if cursor.tables(table=table_name).fetchone():
            print(f"{table_name} table already exist")
        else:
            print(f"Creating {table_name} table")
            cursor.execute(
                f"CREATE TABLE {table_name}("
                f"Id INT PRIMARY KEY AUTO_INCREMENT, "
                f"ServerName VARCHAR(64) NOT NULL, "
                f"DatabaseName VARCHAR(64) NOT NULL, "
                f"RegionName VARCHAR(64) NOT NULL, "
                f"DriverId INT(5) NOT NULL, "
                f"Username VARCHAR(32) NOT NULL, "
                f"Password VARCHAR(64) NOT NULL"
                f");"
            )

            cursor.execute(
                f"ALTER TABLE {table_name} "
                f"ADD FOREIGN KEY (DriverId) "
                f"REFERENCES Driver(Id) "
                f"ON DELETE CASCADE ON UPDATE CASCADE;"
            )

            cursor.close()
            connection.close()
    except Exception as e:
        print(e)
        return
