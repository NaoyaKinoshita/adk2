from google.adk import Workflow

from agents.subagents import city_generator_agent, city_report_agent
from agents.tools import completed_message_function, lookup_time_function

root_agent = Workflow(
    name="root_agent",
    edges=[
        (
            "START",
            city_generator_agent,
            lookup_time_function,
            city_report_agent,
            completed_message_function,
        )
    ],
)
