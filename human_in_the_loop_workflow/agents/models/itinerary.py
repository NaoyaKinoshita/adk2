from pydantic import BaseModel


class Itinerary(BaseModel):
    city: str
    activities: list[str]
