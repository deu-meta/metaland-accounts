from mtl_accounts.database.conn import Base
from sqlalchemy import VARCHAR, Column, ForeignKey


class Users(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "metaland_accounts"}
    email = Column(VARCHAR(50), primary_key=True, index=True)
    role = Column(VARCHAR(50), default="default")
    phone_number = Column(VARCHAR(50), nullable=True)
    provider = Column(VARCHAR(50), nullable=True)
    display_name = Column(VARCHAR(50), nullable=True)
    given_name = Column(VARCHAR(50), nullable=True)
    job_title = Column(VARCHAR(50), nullable=True)


class Minecraft_Account(Base):
    __tablename__ = "minecraft_account"
    __table_args__ = {"schema": "metaland_accounts"}
    id = Column(VARCHAR(50), primary_key=True, index=True)
    user_email = Column(VARCHAR(50), ForeignKey("metaland_accounts.users.email"))
    provider = Column(VARCHAR(50), nullable=True)
    display_name = Column(VARCHAR(50), nullable=True)
