from google.adk import Agent

from agents.prompts import tech_report_instruction

tech_report_agent = Agent(
    name="tech_report_agent",
    model="gemini-2.5-flash",
    instruction=tech_report_instruction(),
    output_schema=str,
)
