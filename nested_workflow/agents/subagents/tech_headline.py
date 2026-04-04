from google.adk import Agent

from agents.prompts import tech_headline_instruction

tech_headline_agent = Agent(
    name="tech_headline_agent",
    model="gemini-2.5-flash",
    instruction=tech_headline_instruction(),
    output_schema=str,
)
