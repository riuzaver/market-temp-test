#!/usr/bin/env python3
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.exc import ProgrammingError
from sqlalchemy import text

import asyncio

import models
from config import settings as s
from db import db_url

psql_url = (
    f"postgresql+asyncpg://"
    f"{s.DATABASE_USER}:"
    f"{s.DATABASE_PASSWORD}@"
    f"{s.DATABASE_HOST}:"
    f"{s.DATABASE_PORT}"
)


def check_test_db():
    if s.DATABASE_HOST not in ("localhost", "127.0.0.1", "postgres"):
        print(s.DATABASE_HOST)
        raise Exception("Use local database only!")


async def setup_db_for_tests(create_tables: bool = True):
    check_test_db()
    e = create_async_engine(psql_url)
    async with e.begin() as conn:
        await conn.execute(text("commit"))
        await conn.execute(text(f"drop database if exists {s.DATABASE_DB}"))
        await conn.execute(text("commit"))
        await conn.execute(text(f"create database {s.DATABASE_DB}"))
        await conn.execute(text("commit"))

    await e.dispose()

    e = create_async_engine(db_url)
    if create_tables:
        async with e.begin() as conn:
            await conn.run_sync(models.Model.metadata.create_all)

    await e.dispose()


def sync_setup_db_for_tests(create_tables: bool = True):
    asyncio.run(setup_db_for_tests(create_tables))


if __name__ == "__main__":
    import typer

    typer.run(sync_setup_db_for_tests)
