import os
from db_connectors.mongo_connector import upload_csv_to_mongo
from db_connectors.mysql_connector import upload_csv_to_mysql

# Paths to CSVs
mongo_csv_path = os.path.join("csv_data", "sales1.csv")
mysql_csv_path = os.path.join("csv_data", "sales2.csv")
mysql_table_name = "sales_data"

def main():
    print("Uploading to MongoDB...")
    upload_csv_to_mongo(mongo_csv_path)

    print("Uploading to MySQL...")
    upload_csv_to_mysql(mysql_csv_path, mysql_table_name)

    print("✅ All data uploaded successfully!")

if __name__ == "__main__":
    main()
