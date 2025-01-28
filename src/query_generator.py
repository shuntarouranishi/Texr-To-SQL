import openai
import re
from dotenv import load_dotenv
import os

# 環境変数の読み込み
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_sql(prompt: str) -> str:
    """
    自然言語プロンプトからSQLクエリを生成し、デバッグ用に記録
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for generating SQL queries."},
                {"role": "user", "content": f"Generate an SQL query for the following request: {prompt}"}
            ],
            max_tokens=1000,
            temperature=0
        )
        generated_sql = response["choices"][0]["message"]["content"]

        # デバッグ: 生成されたSQLをログに記録
        with open("debug_log.txt", "a") as log_file:
            log_file.write(f"\n[Generated SQL]: {generated_sql}\n")

        return generated_sql
    except Exception as e:
        raise RuntimeError(f"Error generating SQL: {str(e)}")

def sanitize_sql(sql: str) -> str:
    """
    サニタイズ処理を行い、SQLクエリを安全な形式に整える。
    クエリ内の最初のSELECT文以降の部分を抽出。
    """
    # 不要な先頭の "sql" を削除
    sql = re.sub(r"^\s*sql\s*", "", sql, flags=re.IGNORECASE)

    # バッククォートを削除
    sql = sql.replace("`", "")

    # SELECT文以降を抽出
    match = re.search(r"SELECT\s+.*", sql, flags=re.IGNORECASE | re.DOTALL)
    if not match:
        raise ValueError("生成されたクエリにSELECT文が見つかりません")

    sanitized_sql = match.group(0)

    # デバッグ: 抽出されたSQLをログに記録
    with open("debug_log.txt", "a") as log_file:
        log_file.write(f"\n[Sanitized SQL]: {sanitized_sql}\n")

    # 最後にセミコロンが複数ある場合を防ぐ
    sanitized_sql = re.sub(r";+", ";", sanitized_sql.strip())

    # 最後のセミコロンを削除
    if sanitized_sql.endswith(";"):
        sanitized_sql = sanitized_sql[:-1]

    return sanitized_sql