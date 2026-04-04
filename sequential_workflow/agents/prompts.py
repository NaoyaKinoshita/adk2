def city_generator_instruction() -> str:
    return """ランダムな都市名を1つ返してください。
      都市名のみを返し、それ以外は何も出力しないでください。"""


def city_report_instruction() -> str:
    return """以下の形式で出力してください:
    現在、{CityTime.city} は {CityTime.time_info} です。"""
