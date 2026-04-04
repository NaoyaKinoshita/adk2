from google.adk import Workflow

from agents.subagents import itinerary_agent, finalize_agent
from agents.tools import (
    request_city,
    request_feedback,
    feedback_router,
    cache_itinerary,
    build_finalize_input,
    final_itinerary_message,
)

root_agent = Workflow(
    name="root_agent",
    edges=[
        (
            "START",
            # Step1: ユーザーに都市名を入力させる (human input)
            request_city,
            # Step2: 入力された都市の観光プランを生成する
            itinerary_agent,
            # Step3: プランを ctx.state にキャッシュして次のノードへ渡す
            #        (ルーティング後は node_input=None になるため state に保存)
            cache_itinerary,
            # Step4: プランをユーザーに提示し、フィードバックを求める (human input)
            request_feedback,
            # Step5: フィードバックの内容でルーティングする
            #   - 「やり直し」→ RESTART (request_city に戻る)
            #   - それ以外   → FINALIZE (build_finalize_input に進む)
            feedback_router,
        ),
        (
            feedback_router,
            {
                "RESTART": request_city,  # 最初のステップに戻る
                "FINALIZE": build_finalize_input,  # state からプランとフィードバックを取得し、後続へ渡す
            },
        ),
        # ルーターにより確定ルートが選ばれた場合、プラン調整と終了メッセージを実行する
        (build_finalize_input, finalize_agent),
        (finalize_agent, final_itinerary_message),
    ],
)
