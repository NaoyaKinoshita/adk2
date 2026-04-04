from google.adk import Workflow

from agents.subagents import sports_agent, tech_agent, science_agent, summary_agent
from agents.tools import join_node

root_agent = Workflow(
    name="root_agent",
    edges=[
        # Step1: 3つのエージェントを並列実行し、それぞれ join_node に集約する
        ("START", sports_agent, join_node),
        ("START", tech_agent, join_node),
        ("START", science_agent, join_node),

        # Step2: すべての並列タスクが完了したら summary_agent を実行する
        (join_node, summary_agent),
    ],
)
