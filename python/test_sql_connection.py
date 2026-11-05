import pyodbc

connection_string = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=UKRoadSafetyDB;"
    "Trusted_Connection=yes;"
    "TrustServerCertificate=yes;"
)

try:
    connection = pyodbc.connect(connection_string)

    cursor = connection.cursor()
    cursor.execute("SELECT DB_NAME()")

    print("SQL Server connection successful!")
    print("Connected database:", cursor.fetchone()[0])

    connection.close()

except pyodbc.Error as error:
    print("SQL Server connection failed:")
    print(error)