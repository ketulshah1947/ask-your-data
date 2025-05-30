import pytest

from src.sql_executor import is_safe_sql


def test_is_safe_sql():
    sql = "SELECT * FROM orders limit 20"
    result = is_safe_sql(sql)
    assert result is True

    sql = "DELETE FROM orders"
    result = is_safe_sql(sql)
    assert result is False
