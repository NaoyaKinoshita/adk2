import logging
import uuid
from typing import Any, Optional

from google.adk.tools import BaseTool, ToolContext

from data_agent.config import (
    EXECUTE_SQL_TOOL_NAME,
    PREVIEW_ROW_COUNT,
    QUERY_RESULT_STATE_PREFIX,
    RESULT_ID_LENGTH,
)

logger = logging.getLogger(__name__)


def stash_query_result(
    tool: BaseTool,
    args: dict[str, Any],
    tool_context: ToolContext,
    tool_response: dict[str, Any],
) -> Optional[dict[str, Any]]:
    """
    execute_sql の全行を state に退避し、LLM にはプレビューだけを返す
    ※行データを LLM のコンテキストに載せない (トークン節約と数値の改変防止)
    """
    if tool.name != EXECUTE_SQL_TOOL_NAME:
        return None

    # エラーや dry run の結果はそのまま LLM に返す
    if not isinstance(tool_response, dict) or "rows" not in tool_response:
        return None
    if tool_response.get("status") != "SUCCESS":
        return None

    rows: list[dict[str, Any]] = tool_response["rows"]
    columns = list(rows[0].keys()) if rows else []
    truncated = bool(tool_response.get("result_is_likely_truncated", False))
    result_id = uuid.uuid4().hex[:RESULT_ID_LENGTH]

    tool_context.state[f"{QUERY_RESULT_STATE_PREFIX}{result_id}"] = {
        "query": args.get("query", ""),
        "columns": columns,
        "rows": rows,
        "truncated": truncated,
    }
    logger.info(
        f"stash_query_result: result_id={result_id}, rows={len(rows)}, "
        f"columns={columns}, truncated={truncated}"
    )

    return {
        "status": "SUCCESS",
        "result_id": result_id,
        "row_count": len(rows),
        "columns": columns,
        "preview_rows": rows[:PREVIEW_ROW_COUNT],
        "result_is_likely_truncated": truncated,
    }
