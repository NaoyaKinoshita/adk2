def topic_generator_instruction() -> str:
    return """
<task_description>
以下のリストからトピックを1つランダムに選択してください。
</task_description>

<topic_list>
- sports
- tech
</topic_list>

<constraints>
- トピック名のみを返してください。それ以外は何も出力しないでください。
</constraints>
"""


def sports_instruction() -> str:
    return """
<task_description>
スポーツに関連する最新の見出しを作成してください。
</task_description>

<constraints>
- 1文で簡潔に記述してください。
</constraints>
"""


def tech_instruction() -> str:
    return """
<task_description>
テクノロジーに関連する最新の見出しを作成してください。
</task_description>

<constraints>
- 1文で簡潔に記述してください。
</constraints>
"""
