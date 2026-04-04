# NOTE: ctx.state を使ったセッションスコープの状態管理。
# ctx.state は EXPERIMENTAL 機能であり、将来的に API が変更される可能性がある。
# 参考: google.adk.agents.context.Context.state
# グローバル変数と異なりセッション単位で分離されるため、複数ユーザーの同時実行でも安全。

import logging
from typing import Optional

from google.adk import Event
from google.adk.agents.context import Context

from agents.models import Itinerary
from agents.tools.state_keys import ITINERARY_KEY, FEEDBACK_KEY

logger = logging.getLogger(__name__)


def cache_itinerary(node_input: Itinerary, ctx: Context) -> Itinerary:
    """itinerary_agent の出力をセッション状態にキャッシュし、そのまま次のノードへ渡す。"""
    logger.info(
        "cache_itinerary: city=%s, activities=%s",
        node_input.city,
        node_input.activities,
    )
    ctx.state[ITINERARY_KEY] = node_input.model_dump_json()
    return node_input


def build_finalize_input(node_input: str | None, ctx: Context) -> str:
    """ctx.state からプランとフィードバックを取得して結合し、finalize_agent に渡す。"""
    itinerary_json = ctx.state.get(ITINERARY_KEY, "")
    feedback = ctx.state.get(FEEDBACK_KEY, "")
    result = (
        f"## 観光プラン\n{itinerary_json}\n\n## ユーザーのフィードバック\n{feedback}"
    )
    logger.info("build_finalize_input: feedback=%s", feedback)
    logger.info(
        "build_finalize_input: returning %d chars to finalize_agent", len(result)
    )
    return result


def final_itinerary_message(node_input: Optional[Itinerary], ctx: Context) -> Event:
    """最終的な観光プランの確定をユーザーに通知するためのメッセージを返す。"""
    itinerary = node_input

    # node_input が None の場合は ctx.state からプランを再構築する（フォールバック）
    if itinerary is None:
        logger.info(
            "final_itinerary_message: node_input is None, falling back to ctx.state"
        )
        itinerary_json = ctx.state.get(ITINERARY_KEY, "")
        if not itinerary_json:
            return Event(message="観光プランを作成できませんでした。")

        itinerary = Itinerary.model_validate_json(itinerary_json)

    activities_text = "\n".join([f"- {a}" for a in itinerary.activities])
    message = (
        f"## 【確定】{itinerary.city}の観光プラン\n\n"
        f"{activities_text}\n\n"
        "観光プランが確定しました！良い旅を！"
    )
    return Event(message=message)


