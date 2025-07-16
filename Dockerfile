FROM python:3.12.3-alpine3.18 AS base

FROM base AS builder

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

# System deps:
RUN apk add build-base unzip wget python3-dev libffi-dev rust cargo openssl-dev

WORKDIR /src

# Generate requirements and install *all* dependencies.
COPY pyproject.toml uv.lock /src/
RUN uv export --format requirements-txt --output-file requirements.txt
RUN pip install --prefix=/runtime --force-reinstall -r requirements.txt

FROM base AS runtime
COPY --from=builder /runtime /usr/local
COPY . /app
WORKDIR /app
EXPOSE 8000/tcp
CMD ["/usr/local/bin/gunicorn", "simple_webfinger.app:create_app()", "-b", "0.0.0.0:8000", "--access-logfile", "-"]