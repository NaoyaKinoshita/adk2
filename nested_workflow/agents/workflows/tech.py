from google.adk import Workflow

from agents.subagents import tech_headline_agent, tech_report_agent

# 子ワークフロー: テック記事を headline → report の順に生成する
tech_workflow = Workflow(
    name="tech_workflow",
    edges=[
        ("START", tech_headline_agent, tech_report_agent),
    ],
)
