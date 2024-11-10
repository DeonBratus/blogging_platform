from pydantic import BaseModel
from datetime import date

class Blog(BaseModel):
    article_title: str 
    content: str

class BlogFullInfo(BaseModel):
    id: int
    article_title: str
    publishing_date: date
    content: str

class BlogSummaryForList(BaseModel):
    id: int
    article_title: str

    class Config:
        orm_mode = True