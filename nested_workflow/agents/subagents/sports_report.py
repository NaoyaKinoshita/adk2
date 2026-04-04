from google.adk import Agent

from agents.prompts import sports_report_instruction

sports_report_agent = Agent(
    name="sports_report_agent",
    model="gemini-2.5-flash",
    instruction=sports_report_instruction(),
    output_schema=str,
)
