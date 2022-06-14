FROM python:3.10-slim as python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

RUN apt-get update && apt-get install -y gcc libffi-dev g++
RUN pip install certifi


RUN pip install poetry

# 
WORKDIR /code

# 
COPY poetry.lock pyproject.toml /code/

# 
COPY ./ /code/
RUN rm -rf /code/.venv
RUN poetry install

# 
CMD ["poetry", "run", "python", "backend/main.py"]
