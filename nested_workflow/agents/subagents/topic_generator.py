from google.adk import Agent

from agents.prompts import topic_generator_instruction

topic_generator_agent = Agent(
    name="topic_generator_agent",
    model="gemini-2.5-flash",
    instruction=topic_generator_instruction(),
    output_schema=str,
)
