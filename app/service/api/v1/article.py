from app.models.articles import Article, ArticleTag
from app.schema.api.v1.article import (
    QueryArticle,
    ArticleSchema,
    ArticlesSchema,
    TagSchema,
)
from app.exc.codes import BIZ_CODE_NOT_EXISTS
from app.utils.api import Response, paginate


async def query_article(query: QueryArticle):
    rows = Article.query_articles(
        query.keyword,
        query.filed_type,
        query.sort,
        query.sort_field,
        query.is_public
    )
    pagination, result = paginate(rows, query.page, query.per_page)
    result = [ArticlesSchema.from_orm(item).dict() for item in result]
    return Response.success(data={"paginate": pagination, "result": result})


def get_article(article_id):
    article = Article.get(article_id)
    if not article:
        return Response.response(code=BIZ_CODE_NOT_EXISTS, message="文章不存在")
    result = ArticleSchema.from_orm(article)
    return Response.success(data=result.dict())


def get_tags():
    tags = ArticleTag.get_all()
    result = [TagSchema.from_orm(item).dict() for item in tags]
    return Response.success(data=result)
