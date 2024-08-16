import pytest
import yaml

from simple_webfinger.app import create_app


@pytest.fixture(scope="module")
def app():
    app = create_app()
    app.webfinger_config = yaml.load(
        open("examples/example-config.yaml", "r"), yaml.SafeLoader
    )
    yield app
