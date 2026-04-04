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


def sports_headline_instruction() -> str:
    return """
<task_description>
最新のスポーツに関連する魅力的な見出しを作成してください。
</task_description>

<constraints>
- 1文で簡潔に記述してください。
</constraints>
"""


def sports_report_instruction() -> str:
    return """
<task_description>
提供されたスポーツの見出しに基づき、詳細を補足した記事を作成してください。
</task_description>

<constraints>
- 全体で2文構成にしてください。
</constraints>
"""


def tech_headline_instruction() -> str:
    return """
<task_description>
最新のテクノロジーに関連する魅力的な見出しを作成してください。
</task_description>

<constraints>
- 1文で簡潔に記述してください。
</constraints>
"""


def tech_report_instruction() -> str:
    return """
<task_description>
提供されたテクノロジーの見出しに基づき、詳細を補足した記事を作成してください。
</task_description>

<constraints>
- 全体で2文構成にしてください。
</constraints>
"""
