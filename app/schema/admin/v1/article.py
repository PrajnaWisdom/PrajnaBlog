from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class ArticleSchema(BaseModel):
    id: str
    name: str
    introduction: Optional[str]
    cover: Optional[str]
    content: str
    views: int
    likes: int
    tags: List[int]
    article_type: int
    is_public: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class QueryArticle(BaseModel):
    keyword: Optional[str] = None
    field_type: Optional[str] = None
    sort: int = 0
    sort_field: Optional[str] = None
    is_public: Optional[int] = None
    page: int = 1
    per_page: int = 10


class CreateArticleSchema(BaseModel):
    name: str
    introduction: Optional[str]
    cover: Optional[str]
    content: str
    tags: List[int]
    article_type: int
    is_public: bool


class CreateTagSchema(BaseModel):
    name: str


class TagSchema(BaseModel):
    id: int
    name: str
