
# import psycopg2
# import pandas as pd
# import sys

# df = pd.read_excel('SARepeatData_June24.xlsx', sheet_name = 'Summary')
# filtered_df = df[(df["Platform"] == "UBR") & (df["Grand Total"] > 2)]
# print("Filtered DataFrame shape:", filtered_df)
# for index, row in filtered_df.iterrows():   
#     data = (
#         row["Circuit ID"] if pd.notna(row["Circuit ID"]) else None,
#         # row["Circle"] if pd.notna(row["Circle"]) else None,
#         # row["Top 50/ROC"] if pd.notna(row["Top 50/ROC"]) else None,
#         # row["Platform"] if pd.notna(row["Platform"]) else None,
#         # row["April'24"] if pd.notna(row["April'24"]) else None,
#         # row["May'24"] if pd.notna(row["May'24"]) else None,
#         # row["June'24"] if pd.notna(row["June'24"]) else None,
#         # row["Grand Total"] if pd.notna(row["Grand Total"]) else None,
#     )
#     print(index, data)
# import pandas as pd
# from sqlalchemy import create_engine

# # Create a database connection
# engine = create_engine('postgresql://psqladm:R%e6DgyQ@10.19.71.176:5432/pms_db')

# try:
#     # Connect to the database
#     with engine.connect() as connection:
#         print("Connected to the database")

#         # Execute a query
#         query = "SELECT * FROM site_type_data LIMIT 1"
#         result = connection.execute(query)

#         # Fetch the result of the query (optional, since we are limiting the result to 1)
#         row = result.fetchone()

#         if row:
#             print("Query executed successfully, fetched data:")
#             print(row)
#         else:
#             print("No data found")

# except Exception as e:
#     print(f"An error occurred: {e}")
# finally:
#     # Ensures connection is closed automatically when using the 'with' context
#     print("Connection closed.")

# from sqlalchemy import create_engine
# from urllib.parse import quote_plus

# # URL-encode the password
# password = 'R%e6DgyQ'
# encoded_password = quote_plus(password)

# # Explicitly specify the psycopg2 driver in the connection string
# engine = create_engine(f'postgresql+psycopg2://psqladm:{encoded_password}@10.19.71.176:5432/pms_db')

# try:
#     # Connect to the database
#     with engine.connect() as connection:
#         print("Connected to the database")

#         # Execute a query
#         query = "SELECT * FROM site_type_data LIMIT 1"
#         result = connection.execute(query)

#         # Fetch the result of the query
#         row = result.fetchone()

#         if row:
#             print("Query executed successfully, fetched data:")
#             print(row)
#         else:
#             print("No data found")

# except Exception as e:
#     print(f"An error occurred: {e}")
# finally:
#     print("Connection closed.")

# import psycopg2

# # Database connection details
# host = "10.19.71.176"
# database = "pms_db"
# user = "psqladm"
# password = "R%e6DgyQ"

# # Establish the connection using psycopg2
# try:
#     connection = psycopg2.connect(
#         host=host,
#         database=database,
#         user=user,
#         password=password
#     )
#     cursor = connection.cursor()

#     # Query to fetch data
#     query = "SELECT * FROM site_type_data LIMIT 1"

#     # Execute the query
#     cursor.execute(query)

#     # Fetch the result
#     result = cursor.fetchone()
    
#     if result:
#         print("Query executed successfully, fetched data:")
#         print(result)
#     else:
#         print("No data found")

# except Exception as e:
#     print(f"An error occurred: {e}")
# finally:
#     if connection:
#         cursor.close()
#         connection.close()
#     print("Connection closed.")


import pandas as pd
from sqlalchemy import create_engine
import psycopg2
from sqlalchemy import text

# Direct psycopg2 connection
conn = psycopg2.connect(
    host="10.19.71.176",
    database="pms_db",
    user="psqladm",
    password="R%e6DgyQ"
)

# Create SQLAlchemy engine that connects to PostgreSQL via psycopg2 directly
engine = create_engine('postgresql+psycopg2://', creator=lambda: conn)

# SQL query to run
query = "SELECT * FROM site_type_data LIMIT 1"

try:
    # Execute query using pandas with SQLAlchemy engine
    df = pd.read_sql(query, engine)
    print("Query executed successfully, fetched data:")
    print(df)
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    conn.close()
    print("Connection closed.")


