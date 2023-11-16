# syntax=docker/dockerfile:1.6
FROM --platform=$BUILDPLATFORM python:3.11-alpine

WORKDIR /app

COPY requirements.txt /app
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements.txt

COPY app.py /app

ENTRYPOINT ["python3"]
CMD ["app.py"]
