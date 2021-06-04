from datetime import datetime
from sqlalchemy import Column, Boolean, DateTime
from sqlalchemy.orm import as_declarative, declarative_mixin

from app.corelibs.store import session


@as_declarative()
class Base(object):

    created_at = Column(DateTime, default=datetime.now, nullable=False, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, nullable=False, onupdate=datetime.now, comment="更新时间")

    @classmethod
    def create(cls, _commit=True, **kwargs):
        obj = cls(**kwargs)
        obj.save(_commit)
        return obj

    def save(self, _commit):
        try:
            session.add(self)
            if _commit:
                session.commit()
        except Exception:
            session.rollback()
            raise

    def update(self, _commit=True, **kwargs):
        for k, v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)
        self.save(_commit)
        return self

    def delete(self, _hard=False, _commit=True):
        if hasattr(self, "deleted") and not _hard:
            self.update(False, deleted=True, deleted_at=datetime.now())
        else:
            session.delete(self)
        if _commit:
            session.commit()


@declarative_mixin
class DeleteTimestampMixin(object):

    deleted = Column(Boolean(), default=False, nullable=False, comment="是否删除")
    deleted_at = Column(DateTime(), nullable=True, comment="删除时间")
