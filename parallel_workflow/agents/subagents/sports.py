from google.adk import Agent

from agents.prompts import sports_instruction

sports_agent = Agent(
    name="sports_agent",
    model="gemini-2.5-flash",
    instruction=sports_instruction(),
    output_schema=str,
)
