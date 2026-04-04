import logging

from google.adk import Event
from google.adk.agents.context import Context

from agents.tools.state_keys import FEEDBACK_KEY

logger = logging.getLogger(__name__)


def feedback_router(node_input: str, ctx: Context) -> Event:
    """フィードバックを state に保存し、内容に応じてルーティングする。
    - 「やり直し」を含む場合 → RESTART (request_city に戻る)
    - それ以外              → FINALIZE (build_finalize_input に進む)

    NOTE: ルーティング後の遷移先ノードには node_input が None で渡されるため、
    フィードバックを ctx.state に保存して引き継ぐ。
    """
    ctx.state[FEEDBACK_KEY] = node_input
    if "やり直し" in node_input:
        logger.info("feedback_router: route=RESTART")
        return Event(route="RESTART")
    logger.info(f"feedback_router: route=FINALIZE, feedback={node_input}")
    return Event(route="FINALIZE")
