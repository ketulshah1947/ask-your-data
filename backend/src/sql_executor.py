from sqlglot import parse_one, exp
from sqlglot.errors import ParseError
from sqlalchemy import text
from src.logger import logger
from src.db_engine import db_engine

FORBIDDEN_NODES = {
    exp.Insert, exp.Delete, exp.Update, exp.Drop, exp.Create, exp.Alter
}


def is_safe_sql(sql: str) -> bool:
    try:
        # Attempt to parse one SQL expression only
        parsed = parse_one(sql, error_level="raise")

        # Root must be a SELECT or WITH (CTE)
        if not isinstance(parsed, (exp.Select, exp.With)):
            return False

        # Traverse AST and check for forbidden nodes
        for node in parsed.walk():
            if isinstance(node, tuple(FORBIDDEN_NODES)):
                return False

        return True
    except ParseError:
        return False


def run_sql(sql: str) -> list[dict]:
    try:
        with db_engine.connect() as conn:
            result = conn.execute(text(sql))
            return [dict(row._mapping) for row in result]
    except Exception as err:
        logger.exception(f"Failed to execute query with an error: {err}", err)
        return []
