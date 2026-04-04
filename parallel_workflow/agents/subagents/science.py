from google.adk import Agent

from agents.prompts import science_instruction

science_agent = Agent(
    name="science_agent",
    model="gemini-2.5-flash",
    instruction=science_instruction(),
    output_schema=str,
)
