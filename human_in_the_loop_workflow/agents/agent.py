from google.adk import Workflow

from agents.subagents import itinerary_agent, finalize_agent
from agents.tools import request_city, request_feedback

root_agent = Workflow(
    name="root_agent",
    edges=[
        (
            "START",
            # Step1: ユーザーに都市名を入力させる (human input)
            request_city,
            # Step2: 入力された都市の観光プランを生成する
            itinerary_agent,
            # Step3: 生成したプランをユーザーに提示し、フィードバックを求める (human input)
            request_feedback,
            # Step4: フィードバックを反映した最終プランを生成する
            finalize_agent,
        )
    ],
)
