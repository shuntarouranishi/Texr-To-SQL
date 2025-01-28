import pyodbc
from dotenv import load_dotenv
import os

# 環境変数をロード
load_dotenv()

try:
    # データベース接続
    connection = pyodbc.connect(
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={os.getenv('DB_HOST')},{os.getenv('DB_PORT')};"
        f"DATABASE={os.getenv('DB_NAME')};"
        f"UID={os.getenv('DB_USER')};"
        f"PWD={os.getenv('DB_PASSWORD')};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )
    print("Database connection established.")

    # クエリの実行
    query = "SELECT * FROM patients;"
    cursor = connection.cursor()
    cursor.execute(query)

    # 結果の表示
    columns = [column[0] for column in cursor.description]
    results = cursor.fetchall()
    print("Query results:")
    for row in results:
        print(dict(zip(columns, row)))

    # 接続を閉じる
    cursor.close()
    connection.close()

except Exception as e:
    print(f"Error: {e}")
