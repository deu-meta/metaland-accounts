from mtl_accounts.database.conn import Base
from sqlalchemy import VARCHAR, Column, ForeignKey


class Users(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "metaland_accounts"}
    mail = Column(VARCHAR(50), primary_key=True, index=True)
    role = Column(VARCHAR(50), default="default")
    phone = Column(VARCHAR(50), nullable=True)
    provider = Column(VARCHAR(50), nullable=True)
    displayName = Column(VARCHAR(50), nullable=True)
    givenName = Column(VARCHAR(50), nullable=True)
    jobTitle = Column(VARCHAR(50), nullable=True)


class Minecraft_Account(Base):
    __tablename__ = "minecraft_account"
    __table_args__ = {"schema": "metaland_accounts"}
    id = Column(VARCHAR(50), primary_key=True, index=True)
    user_mail = Column(VARCHAR(50), ForeignKey("metaland_accounts.users.mail"))
    provider = Column(VARCHAR(50), nullable=True)
    displayName = Column(VARCHAR(50), nullable=True)
