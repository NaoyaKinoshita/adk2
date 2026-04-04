from google.adk.events import RequestInput

from agents.models import Itinerary


async def request_city():
    """ユーザーに観光したい都市名の入力を求める。"""
    yield RequestInput(
        message="観光したい都市名を入力してください:",
        response_schema={"city": "str"},
    )


async def request_feedback(node_input: Itinerary):
    """生成された観光プランをユーザーに提示し、フィードバックを求める。"""
    yield RequestInput(
        message=(
            f"以下の観光プランを確認してください:\n{node_input}\n\n"
            "修正の要望があれば入力してください。なければ「OK」と入力してください。\n"
            "最初からやり直したい場合は「やり直し」と入力してください。"
        ),
        payload=node_input,
        response_schema={"feedback": "str"},
    )
