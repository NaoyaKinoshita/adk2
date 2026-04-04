import logging

from google.adk import Event

from agents.tools.state_keys import FEEDBACK_KEY

logger = logging.getLogger(__name__)


def feedback_router(node_input: str) -> Event:
    """フィードバックを state に保存し、内容に応じてルーティングする。
    ドキュメントの推奨に従い、Event の state パラメータで状態を更新する。
    """
    if "やり直し" in node_input:
        logger.info("feedback_router: route=RESTART")
        return Event(route="RESTART", state={FEEDBACK_KEY: node_input})

    logger.info(f"feedback_router: route=FINALIZE, feedback={node_input}")
    return Event(route="FINALIZE", state={FEEDBACK_KEY: node_input})
