from google.adk import Agent
from google.adk.models import Gemini
from google.adk.tools.agent_tool import AgentTool
from google.genai import types

from data_agent.agent import data_agent
from data_agent.config import GEMINI_MODEL, LLM_RETRY_OPTIONS, LLM_TIMEOUT_MS
from ui_agent.prompts import ui_agent_instruction
from ui_agent.tools import render_chart

root_agent = Agent(
    name="ui_agent",
    model=Gemini(model=GEMINI_MODEL, retry_options=LLM_RETRY_OPTIONS),
    instruction=ui_agent_instruction(),
    tools=[
        # Step1: データ取得 (Step2 で Agent Runtime 上のリモートエージェントに差し替える)
        AgentTool(agent=data_agent),
        # Step2: 取得結果をチャートとしてフロントに描画させる
        render_chart,
    ],
    generate_content_config=types.GenerateContentConfig(
        http_options=types.HttpOptions(timeout=LLM_TIMEOUT_MS),
    ),
)
