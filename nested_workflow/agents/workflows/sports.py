from google.adk import Workflow

from agents.subagents import sports_headline_agent, sports_report_agent

# 子ワークフロー: スポーツ記事を headline → report の順に生成する
sports_workflow = Workflow(
    name="sports_workflow",
    edges=[
        ("START", sports_headline_agent, sports_report_agent),
    ],
)
