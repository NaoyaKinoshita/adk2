from google.adk import Event

from agents.models import CityTime


def lookup_time_function(node_input: str) -> CityTime:
    """Simulate returning the current time in the specified city."""
    return CityTime(time_info="10:10 AM", city=node_input)


def completed_message_function(node_input: str) -> Event:
    return Event(
        message=f"{node_input}\n WORKFLOW COMPLETED.",
    )
