import logging
import os

from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

DATABASE = f'postgresql://{os.getenv("POSTGRESQL_USER")}:{os.getenv("POSTGRESQL_PASSWORD")}@{os.getenv("POSTGRESQL_HOST")}:{os.getenv("POSTGRESQL_PORT")}/{os.getenv("POSTGRESQL_DATABASE")}?client_encoding=utf8'


def _database_exist(engine, schema_name):
    query = f"SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = '{schema_name}'"
    with engine.connect() as conn:
        result_proxy = conn.execute(query)
        result = result_proxy.scalar()
        return bool(result)


def _drop_database(engine, schema_name):
    with engine.connect() as conn:
        conn.execute(f"DROP DATABASE {schema_name};")


def _create_database(engine, schema_name):
    with engine.connect() as conn:
        conn.execute(f"CREATE DATABASE {schema_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;")


class SQLAlchemy:
    def __init__(self, app: FastAPI = None):
        self._engine = None
        self._session = None
        if app is not None:
            self.init_app(app=app)

    def init_app(self, app: FastAPI):
        database_url = DATABASE

        self._engine = create_engine(database_url)

        self._session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=self._engine))

        @app.on_event("startup")
        def startup():
            self._engine.connect()
            logging.info("DB connected.")

        @app.on_event("shutdown")
        def shutdown():
            self._session.close_all()
            self._engine.dispose()
            logging.info("DB disconnected")

    def get_db(self):
        """
        요청마다 DB 세션 유지 함수
        :return:
        """
        if self._session is None:
            raise Exception("must be called 'init_app'")
        db_session = None
        try:
            db_session = self._session()
            yield db_session
        finally:
            db_session.close()

    @property
    def session(self):
        return self.get_db

    @property
    def engine(self):
        return self._engine


db = SQLAlchemy()
Base = declarative_base()
