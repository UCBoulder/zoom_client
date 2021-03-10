"""
Zoom controller. Assists with performing work using Zoom API

By: Dave Bunten

License: MIT - see LICENSE
"""

import os
import sys
import logging
import json
import time
import zoom_client.model as model
import zoom_client.api_client as api_client
import zoom_client.modules.users as users
import zoom_client.modules.group as group
import zoom_client.modules.report as report
import zoom_client.modules.dashboard as dashboard

# set recursion limit higher for rate limitations functions
sys.setrecursionlimit(20000)


class controller:
    def __init__(self, config_data, *args, **kwargs):
        """
        params:
            model: complementary model for storing various zoom data related to this controller
            run_path: root path where the application is being run from on the system
        """
        self.model = model.model()
        self.config_data = config_data
        self.api_client = self.create_api_client(config_data)
        self.users = users.users(self)
        self.group = group.group(self)
        self.report = report.report(self)
        self.dashboard = dashboard.dashboard(self)

    def create_api_client(self, config_data):
        """
        Loads configuration file data and creates new zoom api client using api_client

        params:
            config_data: dictionary containing information relevant to setting up zoom api connection

        returns:
            Configured zoom web api client object
        """

        return api_client.client(
            config_data["root_request_url"],
            config_data["api_key"],
            config_data["api_secret"],
            config_data["data_type"],
        )
