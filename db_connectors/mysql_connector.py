import pandas as pd
import mysql.connector
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# 🚀 Upload CSV to MySQL using mysql.connector
def upload_csv_to_mysql(csv_path, table_name="sales_data2"):
    try:
        load_dotenv()
        host = os.getenv("MYSQL_HOST")
        user = os.getenv("MYSQL_USER")
        password = os.getenv("MYSQL_PASSWORD")
        database = os.getenv("MYSQL_DB")

        # Connect to MySQL using mysql.connector
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        cursor = conn.cursor()
        print("✅ Connected to MySQL")

        # Load CSV
        df = pd.read_csv(csv_path)
        print("✅ CSV loaded successfully")

        # Auto-create table based on CSV columns (all as TEXT for simplicity)
        columns = ", ".join([f"`{col}` TEXT" for col in df.columns])
        create_table_query = f"CREATE TABLE IF NOT EXISTS `{table_name}` ({columns});"
        cursor.execute(create_table_query)
        print("✅ Table ready")

        # Insert rows
        for _, row in df.iterrows():
            placeholders = ", ".join(["%s"] * len(row))
            insert_query = f"INSERT INTO `{table_name}` VALUES ({placeholders})"
            cursor.execute(insert_query, tuple(row))
        conn.commit()
        print("✅ Data inserted successfully")

        # Close
        cursor.close()
        conn.close()

    except Exception as e:
        print(f"❌ Upload to MySQL failed: {e}")

# ✅ Fetch data using SQLAlchemy (warning-free)
def get_mysql_data(table_name="sales_data2"):
    try:
        load_dotenv()
        host = os.getenv("MYSQL_HOST")
        user = os.getenv("MYSQL_USER")
        password = os.getenv("MYSQL_PASSWORD")
        database = os.getenv("MYSQL_DB")

        # Create SQLAlchemy engine
        connection_str = f"mysql+pymysql://{user}:{password}@{host}/{database}"
        engine = create_engine(connection_str)

        # Run query using pandas
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql(query, engine)
        return df.to_dict(orient="records")

    except Exception as e:
        print(f"❌ MySQL fetch failed: {e}")
        return []

# 🧪 Direct test (optional)
if __name__ == "__main__":
    upload_csv_to_mysql("csv_data/sales2.csv", "sales_data2")
    data = get_mysql_data("sales_data2")
    print(data[:3])  # show just a few rows to check
