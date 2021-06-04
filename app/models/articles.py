import shortuuid
from sqlalchemy import Column, Integer, String, TEXT, Boolean, Index, JSON, func, UniqueConstraint

from app.models.base import Base, DeleteTimestampMixin
from app.corelibs.store import session
from app.utils.util import escape_like


class Article(Base, DeleteTimestampMixin):
    """文章"""

    __tablename__ = "article"

    __table_args__ = (
        UniqueConstraint("name", "deleted", "deleted_at"),
    )

    id = Column(
        String(32),
        default=shortuuid.uuid,
        primary_key=True,
        nullable=False,
        comment="ID"
    )
    name = Column(String(125), nullable=False, comment="名称")
    introduction = Column(String(255), nullable=True, comment="简介")
    cover = Column(String(255), nullable=True, comment="封面")
    content = Column(TEXT, nullable=False, comment="正文")
    views = Column(Integer, nullable=False, default=0, comment="浏览量")
    likes = Column(Integer, nullable=False, default=0, comment="点赞数")
    tags = Column(JSON, nullable=False, comment="标签")
    article_type = Column(Integer, nullable=False, comment="类型：0原创，1转载")
    is_public = Column(Boolean, nullable=False, default=True)

    @classmethod
    def get(cls, id):
        return session.query(cls).get(id)

    @classmethod
    def get_by_name(cls, name, bans=None):
        query = session.query(cls).filter(
            cls.name == name,
            cls.deleted == False  # noqa
        )
        if bans:
            query = query.filter(
                cls.id != bans
            )
        return query.first()

    @classmethod
    def query_articles(cls, keyword=None, field_type=None, sort=0, sort_field=None, tags=None, article_type=None,
                       is_public=None):
        query = session.query(cls)
        if keyword and field_type:
            field_type = getattr(cls, field_type)
            query = query.filter(
                field_type.likes("%" + escape_like(keyword) + "%")
            )
        if tags:
            query = query.filter(
                func.json_contains(
                    func.json_extract(cls.tags, "$.*"),
                    func.json_arry(*tags)
                )
            )
        if article_type is not None:
            query = query.filter(
                cls.article_type == article_type
            )
        if is_public is not None:
            query = query.filter(
                cls.is_public == is_public
            )
        if sort_field:
            sort_field = getattr(cls, sort_field)
            if sort == -1:
                sort_field = sort_field.desc()
            query = query.order_by(sort_field)
        query = query.order_by(cls.created_at.desc())
        return query


class Comment(Base, DeleteTimestampMixin):
    """评论"""

    __tablename__ = "comment"

    __table_args__ = (
        Index("idx_article", "article_id"),
        Index("idx_pid", "pid")
    )

    id = Column(String(32), nullable=False, primary_key=True, default=shortuuid.uuid, comment="ID")
    content = Column(TEXT, nullable=False, comment="内容")
    likes = Column(Integer, nullable=False, default=0, comment="点赞数")
    article_id = Column(String(32), nullable=False, comment="博客ID")
    pid = Column(String(32), nullable=False, default="0", comment="上级评论")


class ArticleTag(Base, DeleteTimestampMixin):
    """标签"""

    __tablename__ = "article_tag"

    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True, comment="ID")
    name = Column(String(32), nullable=False, comment="名称")

    @classmethod
    def get_by_name(cls, name, bans=None):
        query = session.query(cls).filter(
            cls.name == name,
            cls.deleted == False  # noqa
        )
        if bans:
            query = query.filter(
                cls.id != bans
            )
        return query.first()

    @classmethod
    def get_all(cls):
        query = session.query(cls).filter(
            cls.deleted == False  # noqa
        )
        return query.all()

    @classmethod
    def get(cls, id):
        return session.query(cls).get(id)
