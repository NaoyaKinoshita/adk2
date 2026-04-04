from google.adk import Agent

from agents.models import Itinerary
from agents.prompts import itinerary_instruction

itinerary_agent = Agent(
    name="itinerary_agent",
    model="gemini-2.5-flash",
    instruction=itinerary_instruction(),
    output_schema=Itinerary,
)
