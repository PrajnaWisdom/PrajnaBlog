import shortuuid
from sqlalchemy import Column, UniqueConstraint, String, Boolean

from app.models.base import Base
from app.corelibs.store import session
from app.utils.werkzeug import generate_password_hash, check_password_hash


class AdminUser(Base):
    """管理员"""

    __tablename__ = "admin_user"

    __table_args__ = (
        UniqueConstraint("account"),
    )

    id = Column(
        String(32),
        default=shortuuid.uuid,
        nullable=False,
        primary_key=True,
        comment="管理员ID"
    )
    account = Column(String(64), nullable=False, comment="管理员账号")
    _password = Column("password", String(128), nullable=False, comment="密码")
    nickname = Column(String(64), nullable=False, comment="昵称")
    avatar = Column(String(255), nullable=True, comment="头像")
    enabled = Column(Boolean, nullable=False, default=True, comment="是否启用")

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self._password, password)

    @classmethod
    def get_by_account(cls, account, enabled=True):
        query = session.query(cls).filter(
            cls.account == account,
            cls.enabled == enabled
        ).first()
        return query
