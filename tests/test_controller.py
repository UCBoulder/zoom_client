""" pytest tests for zoom_client client """
import os
import sys

sys.path.insert(0, os.getcwd())
from zoom_client.client import Client


def test_init():
    """ Basic test initialization of zoom client """
    config_data = {
        "root_request_url": "",
        "api_key": "",
        "api_secret": "",
        "data_type": "",
    }

    zoom = Client(config_data)

    assert hasattr(zoom, "generate_jwt")
    assert hasattr(zoom, "do_request")
