import pyodbc
import traceback
import os
from dotenv import load_dotenv
from src.query_generator import sanitize_sql

# 環境変数をロード
load_dotenv()

def execute_sql(query: str):
    """
    SQL文をデータベースで実行し、結果を返す
    """
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

        # サニタイズ処理
        sanitized_query = sanitize_sql(query)

        # クエリの実行
        cursor = connection.cursor()
        cursor.execute(sanitized_query)

        # SELECT 文の場合は結果を取得
        result = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        result = [dict(zip(columns, row)) for row in result]

        # リソースの解放
        cursor.close()
        connection.close()
        return result

    except pyodbc.ProgrammingError as e:
        print(f"SQL構文エラー: {traceback.format_exc()}")
        return {"error": f"SQL構文エラー: {e}"}
    except Exception as e:
        print(f"Error executing query: {traceback.format_exc()}")
        return {"error": f"Unexpected error: {e}"}
