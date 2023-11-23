import mysql.connector

# Replace with your MariaDB credentials
db_config = {
    'user': 'teety',
    'password': 'top38759',
    'host': '192.168.1.22',  # Replace with your MariaDB server's IP
    'database': 'stock',  # Specify the database name
}

# Connect to the MariaDB server
connection = mysql.connector.connect(**db_config)

try:
    if connection.is_connected():
        print(f'Connected to MariaDB on {db_config["host"]}')

        # Create a cursor
        cursor = connection.cursor()

        # Create a table named 'listitem'
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS listitem (
            id INT AUTO_INCREMENT PRIMARY KEY,
            Item VARCHAR(255),
            Brand VARCHAR(255),
            Category VARCHAR(255),
            Type VARCHAR(255),
            Detail VARCHAR(255),
            Price INT
        )
        '''

        # Execute the SQL query to create the table
        cursor.execute(create_table_query)

        print('Table "listitem" created successfully.')

except mysql.connector.Error as err:
    print(f'Error: {err}')

    # Optionally, print more details about the error
    if hasattr(err, 'errors'):
        for e in err.errors:
            print(f'{e["errno"]} ({e["sqlstate"]}): {e["errmsg"]}')

finally:
    # Close the database connection
    if connection and connection.is_connected():
        connection.close()
        print('Connection closed')
