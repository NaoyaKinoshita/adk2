def city_generator_instruction() -> str:
    return """Return the name of a random city.
      Return only the name, nothing else."""


def city_report_instruction() -> str:
    return """Output following line:
    It is {CityTime.time_info} in {CityTime.city} right now."""
