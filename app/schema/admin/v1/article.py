from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from fastapi import Query


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
    keyword: Optional[str] = Query(None)
    field_type: Optional[str] = Query(None)
    sort: int = Query(0)
    sort_field: Optional[str] = Query(None)
    is_public: Optional[int] = Query(None)
    page: int = Query(1)
    per_page: int = Query(10)


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
