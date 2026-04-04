from pydantic import BaseModel


class Article(BaseModel):
    topic: str
    content: str
