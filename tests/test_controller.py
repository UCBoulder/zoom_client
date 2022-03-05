""" pytest tests for zoom_client client """

import pytest
from zoom_client.client import Client


@pytest.fixture(name="client_config")
def fixture_client_config():
    """fixture config for testing"""
    test_config = {
        "root_request_url": "",
        "api_key": "",
        "api_secret": "",
        "data_type": "",
    }

    return test_config


@pytest.fixture(name="client")
def fixture_client(client_config):
    """fixture for client"""

    zoom = Client(client_config)

    return zoom


def test_client_init(client):
    """Basic test initialization of zoom client"""

    assert hasattr(client, "generate_jwt")
    assert hasattr(client, "do_request")


def test_client_generate_jwt(client):
    """test for generate_jwt content for zoom client"""

    jwt_token = client.generate_jwt()

    assert "Authorization" in jwt_token.keys()
    assert "Content-type" in jwt_token.keys()
    assert "Bearer " in jwt_token["Authorization"]
    assert jwt_token["Content-type"] == "application/json"
