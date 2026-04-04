def topic_generator_instruction() -> str:
    return """
以下のリストからトピックをランダムに1つ選び、トピック名のみを返してください。それ以外は何も出力しないでください:
- sports
- tech
"""


def sports_headline_instruction() -> str:
    return """スポーツニュースの見出しを1文で簡潔に書いてください。"""


def sports_report_instruction() -> str:
    return """スポーツニュースの見出しを受け取ります。
その見出しを膨らませた2文の記事を書いてください。"""


def tech_headline_instruction() -> str:
    return """テクノロジーニュースの見出しを1文で簡潔に書いてください。"""


def tech_report_instruction() -> str:
    return """テクノロジーニュースの見出しを受け取ります。
その見出しを膨らませた2文の記事を書いてください。"""
