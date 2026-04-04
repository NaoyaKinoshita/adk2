from google.adk import Agent

from agents.models import CityTime
from agents.prompts import city_report_instruction

city_report_agent = Agent(
    name="city_report_agent",
    model="gemini-2.5-flash",
    input_schema=CityTime,
    instruction=city_report_instruction(),
    output_schema=str,
)
