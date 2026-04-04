from google.adk import Agent

from agents.prompts import sports_headline_instruction

sports_headline_agent = Agent(
    name="sports_headline_agent",
    model="gemini-2.5-flash",
    instruction=sports_headline_instruction(),
    output_schema=str,
)
