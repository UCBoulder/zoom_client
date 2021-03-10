import os
import sys

sys.path.append(os.getcwd())

import pytest

from zoom_client.controller import controller


def test_init():

    config_data = {
        "root_request_url": "",
        "api_key": "",
        "api_secret": "",
        "data_type": "",
    }

    zoom = controller(config_data)

    assert hasattr(zoom, "api_client")

