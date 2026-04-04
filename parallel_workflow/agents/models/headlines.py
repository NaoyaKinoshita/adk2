from pydantic import BaseModel


class Headlines(BaseModel):
    sports: str
    tech: str
    science: str
