def itinerary_instruction() -> str:
    return """
<task_description>
ユーザーが指定した都市の観光プランを作成してください。
</task_description>

<constraints>
- おすすめのスポットを3〜5件リストアップしてください。
- 各スポットには、その魅力や特徴を一言で補足した説明を添えてください。
- 出力は指定された Itinerary スキーマに厳密に準拠してください。
</constraints>
"""


def finalize_instruction() -> str:
    return """
<task_description>
現在の観光プランに対して、ユーザーのフィードバックを反映した「最終的な観光プラン」を作成してください。
</task_description>

<rules>
- フィードバックが「OK」のみの場合: 受け取った元のプランをそのまま出力してください。
- それ以外の場合: フィードバックの内容を徹底的に反映し、不満点を解消した新しいプランに修正してください。
- 元のプランの良い部分は維持し、追加・変更のみを反映させるのが理想です。
</rules>

<output_instructions>
出力は、Itinerary スキーマに従った有効な JSON 形式である必要があります。
指示内容を反映した正確な JSON オブジェクトのみを返してください。
</output_instructions>
"""
