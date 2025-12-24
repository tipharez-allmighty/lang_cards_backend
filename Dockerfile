FROM python:3.13-slim-bookworm

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ADD . /app

WORKDIR /app

RUN uv sync --no-dev --locked

ENV PATH="/app/.venv/bin:$PATH"

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
