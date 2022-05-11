import os
import sys

import pytest
from faker import Faker
from mtl_accounts.main import create_app
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

DATABASE = f'postgresql://{os.getenv("POSTGRESQL_USER")}:{os.getenv("POSTGRESQL_PASSWORD")}@{os.getenv("POSTGRESQL_HOST")}:{os.getenv("POSTGRESQL_PORT")}/{os.getenv("POSTGRESQL_DATABASE")}?client_encoding=utf8'


@pytest.fixture(scope="session")  # 테스트 실행시 한번만 실행
def app():
    app = create_app()
    return app


@pytest.fixture(scope="session")
def session():
    db = create_engine(DATABASE)
    return scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=db))
