from google.adk import Agent

from agents.prompts import summary_instruction

summary_agent = Agent(
    name="summary_agent",
    model="gemini-2.5-flash",
    instruction=summary_instruction(),
    output_schema=str,
)
