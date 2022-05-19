# market-template-ms
### Preparation
- Install [pipenv](https://github.com/pypa/pipenv)
- Install [cookiecutter](https://cookiecutter.readthedocs.io/)
- Install PostgreSQL
- Install Python 3.10
### Creating ms from template
1. Clone repository
```
git clone git@github.com:startupmillio/market-template-ms.git
```
2. Create database for ms
3. Execute and fill in required values
```
cookiecutter market-template-ms/
```
4. Create pipenv developing environment running command inside created folder
```
pipenv install --dev
```
5. Run tests
```
python -m pytest
```