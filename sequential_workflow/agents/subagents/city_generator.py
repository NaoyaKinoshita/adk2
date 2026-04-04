from google.adk import Agent

city_generator_agent = Agent(
    name="city_generator_agent",
    model="gemini-2.5-flash",
    instruction="""Return the name of a random city.
      Return only the name, nothing else.""",
    output_schema=str,
)
