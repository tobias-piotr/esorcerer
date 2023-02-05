# 🔮 esorcerer

[![python](https://img.shields.io/static/v1?label=python&message=3.11&color=informational&logo=python&logoColor=white)](https://www.python.org/)
[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v0.json)](https://github.com/charliermarsh/ruff)
![Continuous Integration](https://github.com/tobiaxs/esorcerer/workflows/CI/badge.svg?branch=main)

## 📝 Table of Contents

- [About](#about)
- [Installation](#installation)

## 📖 About <a name = "about"></a>

Event sourcing dashboard powered with various plugins.

The basic functionalities are exposing API to create events and attaching hooks to react when a specific event occurs. It may look overengineered (and it probably is), but the main idea was to create an app that uses many popular technologies and tools and integrates them into FastAPI app using ports and adapters architecture. Maybe someone can find this setup useful as a boilerplate for another overengineered project.

List of plugins:

- Database ORM (Tortoise-ORM) ✅
- Tasks (Celery, Redis) ✅
- Caching (Redis) ✅
- Search (ElasticSearch) ❌
- Emails (Sendgrid) ❌

PS: I'm still working on it, so don't judge me.

## 💾 Installation <a name = "installation"></a>

Create a new virtual environment (assuming you already have Python installed e.g. via `pyenv`)

```bash
python -m venv venv
```

Activate it

```bash
source ./venv/bin/activate
```

Install requirements for local setup

```bash
pip install -r ./requirements/local.txt
```

Create `.env` file and populate it with proper values. Example file can be found in [here](./infra/example.env).

Build images

```bash
make build
```

Start containers

```bash
make up
```

After that you should be able to reach <http://localhost:8000/eso/api/docs>, which leads to the Swagger docs.
