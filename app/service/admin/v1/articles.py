from app.models.articles import Article, ArticleTag
from app.schema.admin.v1.article import (
    QueryArticle,
    ArticleSchema,
    CreateArticleSchema,
    CreateTagSchema,
    TagSchema,
)
from app.exc.codes import BIZ_CODE_EXISTS, BIZ_CODE_NOT_EXISTS
from app.utils.api import Response, paginate


def query_articles(query: QueryArticle):
    rows = Article.query_articles(
        query.keyword,
        query.filed_type,
        query.sort,
        query.sort_field,
        query.is_public
    )
    pagination, result = paginate(rows, query.page, query.per_page)
    result = [ArticleSchema.from_orm(item).dict() for item in result]
    return Response.success(data={"paginate": pagination, "result": result})


def create_article(create: CreateArticleSchema):
    if Article.get_by_name(create.name):
        return Response.response(code=BIZ_CODE_EXISTS, message="已存在相同名字的文章")
    article = Article.create(**create.dict())
    return Response.success(data={"id": article.id})


def update_article(article_id, update: CreateArticleSchema):
    article = Article.get(article_id)
    if not article:
        return Response.response(code=BIZ_CODE_NOT_EXISTS, message="文章不存在")
    if Article.get_by_name(update.name, bans=article.id):
        return Response.response(code=BIZ_CODE_EXISTS, message="已存在相同名字的文章")
    article.update(**update.dict())
    return Response.success(data={"id": article.id})


def get_article(article_id):
    article = Article.get(article_id)
    if not article:
        return Response.response(code=BIZ_CODE_NOT_EXISTS, message="文章不存在")
    result = ArticleSchema.from_orm(article)
    return Response.success(data=result.dict())


def delete_article(article_id):
    article = Article.get(article_id)
    if not article:
        return Response.response(code=BIZ_CODE_NOT_EXISTS, message="文章不存在")
    article.delete()
    return Response.success(data={"id": article.id})


def create_tag(create: CreateTagSchema):
    if ArticleTag.get_by_name(create.name):
        return Response.response(code=BIZ_CODE_EXISTS, message="已存在相同名字的标签")
    tag = ArticleTag.create(name=create.name)
    return Response.response(data={"id": tag.id})


def update_tag(tag_id, update: CreateTagSchema):
    tag = ArticleTag.get(tag_id)
    if not tag:
        return Response.response(code=BIZ_CODE_NOT_EXISTS, message="标签不存在")
    if ArticleTag.get_by_name(update.name, bans=tag.id):
        return Response.response(code=BIZ_CODE_EXISTS, message="已存在相同名字的标签")
    tag.update(name=update.name)
    return Response.response(data={"id": tag.id})


def delete_tag(tag_id):
    tag = ArticleTag.get(tag_id)
    if not tag:
        return Response.response(code=BIZ_CODE_NOT_EXISTS, message="标签不存在")
    tag.delete()
    return Response.response(data={"id": tag.id})


def get_tags():
    tags = ArticleTag.get_all()
    result = [TagSchema.from_orm(item).dict() for item in tags]
    return Response.success(data=result)
