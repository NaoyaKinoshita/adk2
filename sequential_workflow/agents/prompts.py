def city_generator_instruction() -> str:
    return """
<task_description>
ランダムな都市名を1つ生成してください。
</task_description>

<constraints>
- 都市名のみを返し、それ以外は何も出力しないでください。
- 日本国内または海外の有名な都市を選んでください。
</constraints>
"""


def city_report_instruction() -> str:
    return """
<task_description>
提供された都市名と時刻情報に基づいて、簡潔なレポートを作成してください。
</task_description>

<output_format>
現在、{CityTime.city} は {CityTime.time_info} です。
</output_format>
"""
