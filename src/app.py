import sys

# プロジェクトのルートディレクトリをモジュール検索パスに追加
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(root_dir)
import openai
import streamlit as st
from src.db_connect import execute_sql
from src.query_generator import generate_sql, sanitize_sql
from dotenv import load_dotenv
import os

# 環境変数をロード
load_dotenv()

# OpenAI APIキーの設定
openai.api_key = os.getenv("OPENAI_API_KEY")

# タイトル
st.title("自然言語 → SQLコードツール")

# レイアウト
col1, col2 = st.columns(2)

# 右側: 自然言語入力
with col2:
    st.header("自然言語クエリを入力")
    user_input = st.text_area("クエリを入力してください（例: 50歳以上の患者を取得）", height=200)

# 左側: 生成されたSQLコードの表示
with col1:
    st.header("生成されたSQLコード")
    if user_input.strip():
        try:
            # SQLコードの生成
            generated_sql = generate_sql(user_input)
            sanitized_sql = sanitize_sql(generated_sql)  # サニタイズ処理

            # サニタイズ後のSQLを表示
            st.text_area("SQLコード", value=sanitized_sql, height=200)

            # 実行ボタン
            if st.button("このSQLを実行する"):
                st.write("### 実行中のクエリ")
                st.code(sanitized_sql, language="sql")

                # SQLの実行
                result = execute_sql(sanitized_sql)
                if "error" in result:
                    st.error(f"SQL 実行中にエラーが発生しました: {result['error']}")
                else:
                    st.write("### 実行結果")
                    st.dataframe(result)
        except ValueError as ve:
            st.error(f"SQL生成中にエラーが発生しました: {ve}")
        except Exception as e:
            st.error(f"予期しないエラーが発生しました: {e}")
    else:
        st.warning("クエリを入力してください。")
