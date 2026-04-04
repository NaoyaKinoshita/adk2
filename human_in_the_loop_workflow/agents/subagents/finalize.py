from google.adk import Agent

from agents.models import Itinerary
from agents.prompts import finalize_instruction

finalize_agent = Agent(
    name="finalize_agent",
    model="gemini-2.5-flash",
    instruction=finalize_instruction(),
    output_schema=Itinerary,
)
