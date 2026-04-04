from google.adk import Agent

from agents.prompts import city_generator_instruction

city_generator_agent = Agent(
    name="city_generator_agent",
    model="gemini-2.5-flash",
    instruction=city_generator_instruction(),
    output_schema=str,
)
