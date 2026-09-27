from data_agent.callbacks import stash_query_result
from data_agent.config import PREVIEW_ROW_COUNT, QUERY_RESULT_STATE_PREFIX

from fakes import FakeTool, FakeToolContext

QUERY = "SELECT category, SUM(sales) AS total_sales FROM t GROUP BY category"


def _rows(count: int) -> list[dict]:
    return [{"category": f"c{_i}", "total_sales": _i * 10} for _i in range(count)]


def test_stash_stores_all_rows_and_returns_preview():
    ctx = FakeToolContext()
    rows = _rows(PREVIEW_ROW_COUNT + 3)

    response = stash_query_result(
        FakeTool("execute_sql"),
        {"project_id": "p", "query": QUERY},
        ctx,
        {"status": "SUCCESS", "rows": rows},
    )

    assert response["status"] == "SUCCESS"
    assert response["row_count"] == len(rows)
    assert response["columns"] == ["category", "total_sales"]
    assert response["preview_rows"] == rows[:PREVIEW_ROW_COUNT]
    assert response["result_is_likely_truncated"] is False
    # 全行は LLM への応答ではなく state に保存される
    assert "rows" not in response
    stored = ctx.state[f"{QUERY_RESULT_STATE_PREFIX}{response['result_id']}"]
    assert stored == {
        "query": QUERY,
        "columns": ["category", "total_sales"],
        "rows": rows,
        "truncated": False,
    }


def test_stash_keeps_truncated_flag():
    ctx = FakeToolContext()
    response = stash_query_result(
        FakeTool("execute_sql"),
        {"query": QUERY},
        ctx,
        {"status": "SUCCESS", "rows": _rows(2), "result_is_likely_truncated": True},
    )
    assert response["result_is_likely_truncated"] is True


def test_stash_handles_empty_result():
    ctx = FakeToolContext()
    response = stash_query_result(
        FakeTool("execute_sql"), {"query": QUERY}, ctx, {"status": "SUCCESS", "rows": []}
    )
    assert response["row_count"] == 0
    assert response["columns"] == []


def test_stash_generates_unique_result_ids():
    ctx = FakeToolContext()
    ids = {
        stash_query_result(
            FakeTool("execute_sql"),
            {"query": QUERY},
            ctx,
            {"status": "SUCCESS", "rows": _rows(1)},
        )["result_id"]
        for _ in range(3)
    }
    assert len(ids) == 3
    assert len(ctx.state) == 3


def test_stash_ignores_other_tools():
    ctx = FakeToolContext()
    response = stash_query_result(
        FakeTool("get_table_info"), {}, ctx, {"status": "SUCCESS", "rows": _rows(1)}
    )
    assert response is None
    assert ctx.state == {}


def test_stash_passes_through_errors():
    ctx = FakeToolContext()
    response = stash_query_result(
        FakeTool("execute_sql"),
        {"query": QUERY},
        ctx,
        {"status": "ERROR", "error_details": "Syntax error"},
    )
    assert response is None
    assert ctx.state == {}


def test_stash_passes_through_dry_run():
    ctx = FakeToolContext()
    response = stash_query_result(
        FakeTool("execute_sql"),
        {"query": QUERY, "dry_run": True},
        ctx,
        {"status": "SUCCESS", "dry_run_info": {}},
    )
    assert response is None
    assert ctx.state == {}
