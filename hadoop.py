from impala.dbapi import connect

# Establish the connection parameters
host = '10.19.33.130'
port = 21051
cursor = None
conn = None

# Fixed database name
db_name = 'fas2'

try:
    # Connect to the Impala database
    conn = connect(host=host, port=port)
    print("Connection to Impala successful.")

    cursor = conn.cursor()

    # Get available database names
    cursor.execute("SHOW DATABASES")
    database_names = cursor.fetchall()

    # Extract database names into a list
    db_list = [db[0] for db in database_names]
    #print("Available databases:", db_list)

    # Check if the fixed database exists and use it
    if db_name in db_list:
        cursor.execute(f"USE {db_name}")
        print(f"Using database: {db_name}")

        # Check available tables in the database
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        table_list = [table[0] for table in tables]
        print("Tables in fas2 database:", table_list)

        # Check if the specific table exists
        if 'fct_fault' in table_list:
            # Execute a query to select data from the table
            cursor.execute("SELECT * FROM fct_fault LIMIT 2")
            data = cursor.fetchall()  # Fetch all results
            print("data =",type(data),type(data[0]))
            print(f"\nData from ftc_fault (first 2 records):")
            for row in data:
                print(row)  # Print each row of data
        else:
            print("Table 'ftc_fault' not found in database 'fas2'.")
    else:
        print("Database not found.")
except Exception as e:
    print("Error connecting or executing query:", e)
finally:
    # Ensure cursor and connection are closed safely
    if cursor:
        cursor.close()
    if conn:
        conn.close()
    print("Connection closed.")

