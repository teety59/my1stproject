import mysql.connector
import pandas as pd
from sqlalchemy import create_engine

# Replace with your MariaDB credentials
db_config = {
    'user': 'teety',
    'password': 'top38759',
    'host': '192.168.1.22',  # Replace with your MariaDB server's IP
    'database': 'stock',  # Specify the database name
}

excel_file_path = 'stock.xlsx'  # Replace with the actual path

# Define the structure of the 'listitem' table
table_structure = {
    'Item': 'VARCHAR(255)',
    'Brand': 'VARCHAR(255)',
    'Type1': 'VARCHAR(255)',
    'Type2': 'VARCHAR(255)',
    'Detail': 'VARCHAR(255)',
    'Price': 'INT'
}

connection = None

try:
    # Connect to the MariaDB server using SQLAlchemy
    engine = create_engine(f"mysql+mysqlconnector://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}")

    # Read Excel file into a pandas DataFrame
    df = pd.read_excel(excel_file_path, sheet_name='Data')

    # Verify that DataFrame columns match the table structure
    if set(df.columns) != set(table_structure.keys()):
        raise ValueError("DataFrame columns do not match the table structure")

    # Insert data into the 'listitem' table
    table_name = 'listitem'
    df.to_sql(table_name, con=engine, index=False, if_exists='replace', method='multi', chunksize=500)

    print(f'Data from Excel file inserted into MariaDB table "{table_name}" successfully.')

except mysql.connector.Error as err:
    print(f'Error: {err}')

    # Optionally, print more details about the error
    if hasattr(err, 'errors'):
        for e in err.errors:
            print(f'{e["errno"]} ({e["sqlstate"]}): {e["errmsg"]}')

finally:
    # Close the database connection (Note: SQLAlchemy handles the connection, so no need to close it explicitly)
    print('Operation completed.')
