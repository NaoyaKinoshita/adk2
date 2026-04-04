from google.adk import Workflow

from agents.subagents import topic_generator_agent
from agents.tools import topic_router
from agents.workflows import sports_workflow, tech_workflow

root_agent = Workflow(
    name="root_agent",
    edges=[
        # Step1: トピックを生成し、topic_router で子ワークフローへの分岐先を決定する
        ("START", topic_generator_agent, topic_router),

        # Step2: topic_router が返す Event(route="...") の値で子ワークフローを切り替える
        #   - "RUN_SPORTS_WORKFLOW" → sports_workflow (headline → report)
        #   - "RUN_TECH_WORKFLOW"   → tech_workflow   (headline → report)
        (
            topic_router,
            {
                "RUN_SPORTS_WORKFLOW": sports_workflow,
                "RUN_TECH_WORKFLOW": tech_workflow,
            },
        ),
    ],
)
