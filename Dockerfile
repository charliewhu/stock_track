FROM python:3.12-slim-bookworm

# install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

# install deps
COPY pyproject.toml uv.lock /app/
RUN uv pip install --system -r pyproject.toml

# install application
COPY . /app/
RUN uv pip install --system -e .
