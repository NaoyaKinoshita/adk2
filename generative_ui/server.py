import logging
import os

from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

from ag_ui_adk import ADKAgent, add_adk_fastapi_endpoint  # noqa: E402
from fastapi import FastAPI  # noqa: E402

from ui_agent.agent import root_agent  # noqa: E402

logging.basicConfig(level=logging.INFO)

APP_NAME = "generative_ui"
# 技術検証用の固定ユーザー。本番では認証情報から user_id_extractor で取り出す
DEMO_USER_ID = "demo_user"
# エージェント実行全体 / ツール1回あたりのタイムアウト (秒)
EXECUTION_TIMEOUT_SECONDS = 300
TOOL_TIMEOUT_SECONDS = 180

agent = ADKAgent(
    adk_agent=root_agent,
    app_name=APP_NAME,
    user_id=DEMO_USER_ID,
    use_in_memory_services=True,
    execution_timeout_seconds=EXECUTION_TIMEOUT_SECONDS,
    tool_timeout_seconds=TOOL_TIMEOUT_SECONDS,
)

app = FastAPI(title="Generative UI Agent (AG-UI)")
add_adk_fastapi_endpoint(app, agent, path="/")
