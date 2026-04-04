def sports_instruction() -> str:
    return """
<task_description>
最新のスポーツニュースを想定し、魅力的で見栄えの良い見出しを1つ作成してください。
</task_description>

<constraints>
- 1文で簡潔に記述してください。
</constraints>
"""


def tech_instruction() -> str:
    return """
<task_description>
最新のテクノロジーニュースを想定し、魅力的で見栄えの良い見出しを1つ作成してください。
</task_description>

<constraints>
- 1文で簡潔に記述してください。
</constraints>
"""


def science_instruction() -> str:
    return """
<task_description>
最新のサイエンスニュースを想定し、魅力的で見栄えの良い見出しを1つ作成してください。
</task_description>

<constraints>
- 1文で簡潔に記述してください。
</constraints>
"""


def summary_instruction() -> str:
    return """
<task_description>
提供された複数のニュース見出し（スポーツ、テック、サイエンス）を1つの短いパラグラフに要約してください。
</task_description>

<constraints>
- すべてのトピックを網羅するようにしてください。
- 読者が一目で内容を把握できるように簡潔にまとめてください。
</constraints>
"""
