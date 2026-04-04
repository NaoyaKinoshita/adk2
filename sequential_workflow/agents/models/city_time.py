from pydantic import BaseModel


class CityTime(BaseModel):
    time_info: str
    city: str
