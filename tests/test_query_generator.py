from src.query_generator import natural_language_to_sql

def test_query_generator():
    schema = """
    CREATE TABLE patients (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        age INT,
        gender VARCHAR(10),
        diagnosis_date DATE
    );
    """
    prompt = "List all patients older than 50"
    sql = natural_language_to_sql(prompt, schema)
    assert "SELECT" in sql, "SQL query generation failed"
    assert "patients" in sql, "Generated SQL does not reference the expected table"
