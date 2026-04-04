def topic_generator_instruction() -> str:
    return """
Choose one topic randomly from the following list and return only the topic name, nothing else:
- sports
- tech
"""


def sports_instruction() -> str:
    return """Write a short one-sentence sports news headline."""


def tech_instruction() -> str:
    return """Write a short one-sentence tech news headline."""
