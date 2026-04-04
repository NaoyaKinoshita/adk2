from google.adk import Event


def topic_router(node_input: str) -> Event:
    """Route to the appropriate agent based on the topic."""
    topic = node_input.strip().lower()
    if "sport" in topic:
        return Event(route="RUN_SPORTS_AGENT")
    else:
        return Event(route="RUN_TECH_AGENT")
