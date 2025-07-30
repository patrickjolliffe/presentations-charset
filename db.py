import oracledb
import os

oracledb.init_oracle_client(lib_dir="/Users/patrick/instantclient_23_3")

# Configure Oracle client behavior
os.environ["NLS_LANG"] = "AMERICAN_AMERICA.US7ASCII"

print("Using thick mode:", not oracledb.is_thin_mode())

# Connect to the database
conn = oracledb.connect(user="pdbadmin", password="pdbadmin", dsn="localhost:1521/freepdb1")

cursor = conn.cursor()
cursor.execute("SELECT name FROM dogs")

for row in cursor:
    print(row)

cursor.close()
conn.close()