from fastapi import APIRouter

from app.service.api.v1.article import (
    query_article,
    get_article,
    get_tags,
)
from app.schema.admin.v1.article import (
    QueryArticle,
)


router = APIRouter()


@router.post("/list")
async def api_query_articles(query: QueryArticle):
    return query_article(query)


@router.get("/<article_id>")
async def api_get_article(article_id: str):
    return get_article(article_id)


@router.get("/tag/list")
async def api_get_tags():
    return get_tags()
