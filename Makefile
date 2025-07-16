.venv:
	uv sync --all-extras

.PHONY: tests
tests: .venv
	uv run pytest

lint: .venv
	uv run ruff check --output-format=github --select=E9,F63,F7,F82 --target-version=py37 .
	uv run ruff check --output-format=github --target-version=py37 .

serve-uwsgi:
	SIMPLE_WEBFINGER_CONFIG_FILE="examples/example-config.yaml" uv run gunicorn "simple_webfinger.app:create_app()"

serve:
	DEBUG_METRICS=1 SIMPLE_WEBFINGER_CONFIG_FILE="examples/example-config.yaml" FLASK_DEBUG=1 FLASK_APP="simple_webfinger.app:create_app()" uv run flask run
