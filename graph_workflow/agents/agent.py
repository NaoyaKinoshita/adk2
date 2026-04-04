from google.adk import Workflow

from agents.subagents import topic_generator_agent, sports_agent, tech_agent
from agents.tools import topic_router

root_agent = Workflow(
    name="root_agent",
    edges=[
        # Step1: トピックを生成し、topic_router で分岐先を決定する
        ("START", topic_generator_agent, topic_router),
        # Step2: topic_router が返す Event(route="...") の値でブランチを切り替える
        #   - "RUN_SPORTS_AGENT" → sports_agent
        #   - "RUN_TECH_AGENT"   → tech_agent
        (
            topic_router,
            {
                "RUN_SPORTS_AGENT": sports_agent,
                "RUN_TECH_AGENT": tech_agent,
            },
        ),
    ],
)
