#!/usr/bin/env python3
from sqlalchemy import create_engine
from sqlalchemy.exc import ProgrammingError
import models
from configs import settings as s
from db import DATABASE_URL

psql_url = f"postgresql://{s.DATABASE_USER}:{s.DATABASE_PASSWORD}@{s.DATABASE_HOST}:{s.DATABASE_PORT}"


def check_test_db():
    if s.DATABASE_HOST not in ("localhost", "127.0.0.1", "postgres"):
        print(s.DATABASE_HOST)
        raise Exception("Use local database only!")


def setup_db_for_tests(create_tables: bool = True):
    check_test_db()
    e = create_engine(psql_url)
    conn = e.connect()
    conn.execute("commit")
    conn.execute(f"drop database if exists {s.DATABASE_DB}")
    conn.execute("commit")
    conn.execute(f"create database {s.DATABASE_DB}")
    conn.execute("commit")
    conn.close()

    e = create_engine(DATABASE_URL)
    if create_tables:
        models.Model.metadata.create_all(e)


if __name__ == "__main__":
    import typer

    typer.run(setup_db_for_tests)
