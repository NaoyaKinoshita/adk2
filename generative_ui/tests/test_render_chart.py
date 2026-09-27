import pytest
from pydantic import ValidationError

from data_agent.config import QUERY_RESULT_STATE_PREFIX
from ui_agent.models import ChartSpec
from ui_agent.tools import render_chart

from fakes import FakeToolContext

RESULT_ID = "abc12345"
COLUMNS = ["month", "sales", "orders"]


def _ctx() -> FakeToolContext:
    return FakeToolContext(
        state={
            f"{QUERY_RESULT_STATE_PREFIX}{RESULT_ID}": {
                "query": "SELECT ...",
                "columns": COLUMNS,
                "rows": [{"month": "2026-01", "sales": 100, "orders": 3}],
                "truncated": False,
            }
        }
    )


def test_render_chart_success():
    response = render_chart("line", "月別売上", RESULT_ID, "month", ["sales"], _ctx())
    assert response == {"status": "SUCCESS"}


def test_render_chart_table_ignores_keys():
    response = render_chart("table", "一覧", RESULT_ID, None, [], _ctx())
    assert response == {"status": "SUCCESS"}


def test_render_chart_unknown_result_id():
    response = render_chart("bar", "売上", "missing", "month", ["sales"], _ctx())
    assert response["status"] == "ERROR"
    assert "missing" in response["error_message"]


def test_render_chart_unknown_column():
    response = render_chart("bar", "売上", RESULT_ID, "month", ["profit"], _ctx())
    assert response["status"] == "ERROR"
    assert "profit" in response["error_message"]
    # LLM が自己修正できるよう利用可能なカラムを返す
    assert "sales" in response["error_message"]


def test_render_chart_invalid_chart_type():
    response = render_chart("scatter", "売上", RESULT_ID, "month", ["sales"], _ctx())
    assert response["status"] == "ERROR"


@pytest.mark.parametrize(
    ("chart_type", "x_key", "y_keys"),
    [
        ("bar", None, ["sales"]),
        ("line", "month", []),
        ("pie", "month", ["sales", "orders"]),
    ],
)
def test_chart_spec_rejects_invalid_keys(chart_type, x_key, y_keys):
    with pytest.raises(ValidationError):
        ChartSpec(
            chart_type=chart_type,
            title="t",
            result_id=RESULT_ID,
            x_key=x_key,
            y_keys=y_keys,
        )


def test_chart_spec_missing_columns():
    spec = ChartSpec(
        chart_type="bar",
        title="t",
        result_id=RESULT_ID,
        x_key="month",
        y_keys=["sales", "profit"],
    )
    assert spec.missing_columns(COLUMNS) == ["profit"]
