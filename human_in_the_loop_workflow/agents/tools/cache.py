import logging
from typing import Optional

from google.adk import Event
from agents.models import Itinerary
from agents.tools.state_keys import ITINERARY_KEY

logger = logging.getLogger(__name__)


def cache_itinerary(node_input: Itinerary) -> Event:
    """itinerary_agent の出力をセッション状態に保存し、次のノードへ渡す。
    ドキュメントの推奨に従い、Event の state パラメータを利用。
    """
    logger.info(f"cache_itinerary: city={node_input.city}")
    return Event(
        output=node_input,
        state={ITINERARY_KEY: node_input.model_dump_json()},
    )


def build_finalize_input(
    node_input: str | None, cached_itinerary: str, cached_feedback: str
) -> str:
    """引数インジェクションを利用して state からプランとフィードバックを取得する。
    ドキュメントの推奨に従い、state のキー名と同名の引数で値を受け取る。
    """
    result = (
        f"## 観光プラン\n{cached_itinerary}\n\n## ユーザーのフィードバック\n{cached_feedback}"
    )
    logger.info(f"build_finalize_input: feedback={cached_feedback}")
    logger.info(f"build_finalize_input: returning {len(result)} chars to finalize_agent")
    return result


def final_itinerary_message(
    node_input: Optional[Itinerary], cached_itinerary: str = ""
) -> Event:
    """最終的な観光プランの確定をユーザーに通知するためのメッセージを返す。
    node_input が None の場合は、引数インジェクションされた cached_itinerary を利用する。
    """
    itinerary = node_input

    # node_input が None の場合は state からプランを再構築する（フォールバック）
    if itinerary is None:
        logger.info(
            "final_itinerary_message: node_input is None, falling back to cached_itinerary"
        )
        if not cached_itinerary:
            return Event(message="観光プランを作成できませんでした。")

        itinerary = Itinerary.model_validate_json(cached_itinerary)

    activities_text = "\n".join(
        [f"- {_activity}" for _activity in itinerary.activities]
    )
    message = (
        f"## 【確定】{itinerary.city}の観光プラン\n\n"
        f"{activities_text}\n\n"
        "観光プランが確定しました！良い旅を！"
    )
    return Event(message=message)
