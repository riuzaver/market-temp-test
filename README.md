# market-template-ms
### Preparation
- Install [pipenv](https://github.com/pypa/pipenv)
- Install [cookiecutter](https://cookiecutter.readthedocs.io/)
- Install [cruft](https://pypi.org/project/cruft/)
- Install PostgreSQL
- Install Python 3.10
### Creating ms from template
1. Execute and fill in required values
```
cruft create git+ssh://git@github.com/startupmillio/market-template-ms
```
2. Create pipenv developing environment running command inside created folder
```
pipenv install --dev
```
3. Inside `.secrets.toml` set your local environment variables
4. Create database with
```
python -m tests.setup_test_db
```
4. Run tests
```
py.test
```
5. Run ms
```
uvicorn main:app --reload
```
### Migrations
For creating migration use [alembic](https://alembic.sqlalchemy.org/en/latest/tutorial.html) command (only for models inherited from base class Model)
```
alembic revision --autogenerate -m "Useful migration"
```
And to migrate to the most recent
```
alembic upgrade head
```
### Template update
Check for updates of template with `cruft check` and update with `cruft update`