from sqlalchemy import text

from src.db_engine import db_engine


def get_db_schema_text() -> str:
    with db_engine.connect() as conn:
        result = conn.execute(text("""
            SELECT table_name, column_name, data_type
            FROM information_schema.columns
            WHERE table_schema = 'public'
            ORDER BY table_name, ordinal_position;
        """))
        schema_lines = []
        current_table = None
        for row in result:
            table, column, dtype = row
            if table != current_table:
                schema_lines.append(f"\nTable {table}:")
                current_table = table
            schema_lines.append(f"- {column} ({dtype})")
    return "\n".join(schema_lines)
