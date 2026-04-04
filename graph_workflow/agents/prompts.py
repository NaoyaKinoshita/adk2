def topic_generator_instruction() -> str:
    return """
以下のリストからトピックをランダムに1つ選び、トピック名のみを返してください。それ以外は何も出力しないでください:
- sports
- tech
"""


def sports_instruction() -> str:
    return """スポーツニュースの見出しを1文で簡潔に書いてください。"""


def tech_instruction() -> str:
    return """テクノロジーニュースの見出しを1文で簡潔に書いてください。"""
