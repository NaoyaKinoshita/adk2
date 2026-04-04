from google.adk import Agent

from agents.prompts import tech_instruction

tech_agent = Agent(
    name="tech_agent",
    model="gemini-2.5-flash",
    instruction=tech_instruction(),
    output_schema=str,
)
