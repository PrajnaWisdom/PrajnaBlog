from fastapi import APIRouter

from app.service.admin.v1.articles import (
    query_articles,
    create_article,
    update_article,
    get_article,
    delete_article,
    create_tag,
    update_tag,
    delete_tag,
    get_tags,
)
from app.schema.admin.v1.article import (
    QueryArticle,
    CreateArticleSchema,
    CreateTagSchema,
)


router = APIRouter()


@router.get("/list")
async def admin_query_articles(query: QueryArticle):
    return query_articles(query)


@router.post("/create")
async def admin_create_article(data: CreateArticleSchema):
    return create_article(data)


@router.put("/<article_id>/update")
async def admin_updated_article(article_id: str, data: CreateArticleSchema):
    return update_article(article_id, data)


@router.get("/<article_id>")
async def admin_get_article(article_id: str):
    return get_article(article_id)


@router.delete("/<article_id>")
async def admin_delete_article(article_id):
    return delete_article(article_id)


@router.get("/tag/list")
async def admin_get_tags():
    return get_tags()


@router.post("/tag/create")
async def admin_create_tag(data: CreateTagSchema):
    return create_tag(data)


@router.put("/tag/<tag_id>/update")
async def admin_updated_tag(tag_id: int, data: CreateTagSchema):
    return update_tag(tag_id, data)


@router.delete("/tag/<tag_id>")
async def admin_delete_tag(tag_id: int):
    return delete_tag(tag_id)
