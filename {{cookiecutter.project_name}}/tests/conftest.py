import asyncio
from contextlib import asynccontextmanager
from inspect import isawaitable
from typing import Any
from unittest.mock import patch
from models import Model
import pytest
from fastapi import FastAPI
from graphene_sqlalchemy_core.app import SessionQLApp
from graphene_sqlalchemy_core.middlewares import LoaderMiddleware
from graphql import ASTValidationRule, GraphQLError
from httpx import AsyncClient
from pytest_mock import MockerFixture
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from starlette.background import BackgroundTasks
from starlette.requests import HTTPConnection, Request

from config import settings as st
from db import get_session
from gql.schema import schema
from main import app

db_url = (
    "postgresql+asyncpg://"
    f"{st.DATABASE_USER}:"
    f"{st.DATABASE_PASSWORD}@"
    f"{st.DATABASE_HOST}:"
    f"{st.DATABASE_PORT}/"
    f"{st.DATABASE_DB}"
)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


def check_test_db():
    if (
        st.DATABASE_HOST not in ("localhost", "127.0.0.1", "postgres")
        or "amazonaws" in st.DATABASE_HOST
    ):
        print(db_url)
        raise Exception("Use local database only!")


@pytest.fixture(scope="session")
async def engine():
    check_test_db()

    e = create_async_engine(db_url, echo=False, max_overflow=25)

    try:
        async with e.begin() as con:
            await con.run_sync(Model.metadata.create_all)

        yield e
    finally:
        async with e.begin() as con:
            await con.run_sync(Model.metadata.drop_all)


@pytest.fixture
async def dbsession(engine) -> AsyncSession:
    async with AsyncSession(bind=engine) as session:
        yield session


@pytest.fixture
async def test_client_rest(dbsession: AsyncSession) -> AsyncClient:
    def override_get_db():
        test_db = dbsession
        yield test_db

    app.dependency_overrides[get_session] = override_get_db

    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def test_client_graph(dbsession: AsyncSession) -> AsyncClient:
    class _SessionQLApp(SessionQLApp):
        def __init__(self, *args, **kwargs):
            super().__init__(engine=None, *args, **kwargs)

        @asynccontextmanager
        async def _get_context_value(self, request: HTTPConnection) -> Any:
            if callable(self.context_value):
                context = self.context_value(
                    request=request,
                    background=BackgroundTasks(),
                    session=dbsession,
                )
                if isawaitable(context):
                    context = await context
                yield context
            else:
                yield self.context_value or {
                    "request": request,
                    "background": BackgroundTasks(),
                    "session": dbsession,
                }

    _app = FastAPI()
    _app.add_route(
        path="/graphql",
        route=_SessionQLApp(
            schema=schema,
            middleware=[
                LoaderMiddleware(Model.registry.mappers),
            ],
        ),
    )

    async with AsyncClient(app=_app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def raise_graphql():
    def report_error(self, x, *args, **kwargs):
        raise x

    def gql_error_init(
        self,
        message: str,
        nodes=None,
        source=None,
        positions=None,
        path=None,
        original_error=None,
        extensions=None,
    ):
        raise original_error or Exception(message)

    with patch.object(ASTValidationRule, "report_error", report_error), patch.object(
        GraphQLError, "__init__", gql_error_init
    ):
        yield
