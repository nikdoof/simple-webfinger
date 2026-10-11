import pytest
import yaml

from simple_webfinger.app import create_app


@pytest.fixture(scope="module")
def app():
    app = create_app()
    with open("examples/example-config.yaml", "r") as config_file:
        app.webfinger_config = yaml.safe_load(config_file)
    yield app
