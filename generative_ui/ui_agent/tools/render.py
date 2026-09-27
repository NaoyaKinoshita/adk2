import logging
from typing import Any

from google.adk.tools import ToolContext
from pydantic import ValidationError

from data_agent.config import QUERY_RESULT_STATE_PREFIX
from ui_agent.models import ChartSpec

logger = logging.getLogger(__name__)


def render_chart(
    chart_type: str,
    title: str,
    result_id: str,
    x_key: str | None,
    y_keys: list[str],
    tool_context: ToolContext,
) -> dict[str, Any]:
    """
    クエリ結果をチャートとしてユーザーの画面に表示する。

    Args:
        chart_type: "bar" / "line" / "area" / "pie" / "table" のいずれか。
        title: チャートのタイトル (日本語)。
        result_id: data_agent が返した result_id。
        x_key: 横軸 (pie はラベル) に使うカラム名。table の場合は null。
        y_keys: 縦軸 (pie は値) に使う数値カラム名のリスト。table の場合は空リスト。
    """
    try:
        spec = ChartSpec(
            chart_type=chart_type,
            title=title,
            result_id=result_id,
            x_key=x_key,
            y_keys=y_keys,
        )
    except ValidationError as e:
        logger.warning(f"render_chart: invalid spec, result_id={result_id}, error={e}")
        return {"status": "ERROR", "error_message": str(e)}

    result = tool_context.state.get(f"{QUERY_RESULT_STATE_PREFIX}{spec.result_id}")
    if result is None:
        logger.warning(f"render_chart: result not found, result_id={spec.result_id}")
        return {
            "status": "ERROR",
            "error_message": f"result_id={spec.result_id} のクエリ結果が見つかりません",
        }

    missing = spec.missing_columns(result["columns"])
    if missing:
        logger.warning(
            f"render_chart: unknown columns, result_id={spec.result_id}, missing={missing}"
        )
        return {
            "status": "ERROR",
            "error_message": (
                f"存在しないカラムが指定されています: {missing}。"
                f"利用可能なカラム: {result['columns']}"
            ),
        }

    logger.info(
        f"render_chart: result_id={spec.result_id}, chart_type={spec.chart_type}"
    )
    # 描画はフロントエンドがこのツール呼び出しの引数と state の行データから行う
    return {"status": "SUCCESS"}
