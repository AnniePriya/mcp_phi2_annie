import pandas as pd
import mysql.connector
from dotenv import load_dotenv
import os

def upload_csv_to_mysql(csv_path, table_name="sales_data2"):
    try:
        # Load environment variables
        load_dotenv()
        host = os.getenv("MYSQL_HOST")
        user = os.getenv("MYSQL_USER")
        password = os.getenv("MYSQL_PASSWORD")
        database = os.getenv("MYSQL_DB")

        # Connect to MySQL
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        cursor = conn.cursor()
        print("✅ Connected to MySQL")

        # Read the CSV
        df = pd.read_csv(csv_path)
        print("✅ CSV loaded successfully")

        # Create the table (optional - assumes structure based on DataFrame)
        columns = ", ".join([f"`{col}` TEXT" for col in df.columns])
        create_table_query = f"CREATE TABLE IF NOT EXISTS `{table_name}` ({columns});"
        cursor.execute(create_table_query)
        print("✅ Table ready")

        # Insert data
        for _, row in df.iterrows():
            placeholders = ", ".join(["%s"] * len(row))
            insert_query = f"INSERT INTO `{table_name}` VALUES ({placeholders})"
            cursor.execute(insert_query, tuple(row))
        conn.commit()
        print("✅ Data inserted successfully")

        # Close connections
        cursor.close()
        conn.close()

    except Exception as e:
        print(f"❌ Upload to MySQL failed: {e}")

# For direct testing
if __name__ == "__main__":
    upload_csv_to_mysql("csv_data/sales2.csv", "sales_data2")

def get_mysql_data(table_name="sales_data2"):
    try:
        load_dotenv()
        conn = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DB"),
            
        )

        query = "SELECT * FROM sales_data2"
        df = pd.read_sql(query, conn)
        conn.close()
        return df.to_dict(orient="records")

    except Exception as e:
        print(f"❌ MySQL fetch failed: {e}")
        return []
