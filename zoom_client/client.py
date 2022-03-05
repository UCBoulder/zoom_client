"""
Zoom client class which assists with performing work using Zoom API
"""

import datetime
import logging
import sys

import jwt
import requests
from requests.exceptions import RequestException

from zoom_client.modules import dashboard
from zoom_client.modules import group
from zoom_client.modules import report
from zoom_client.modules import users

# set recursion limit higher for rate limitations functions
sys.setrecursionlimit(20000)


class Client:
    """Zoom client class which assists with performing work using Zoom API"""

    def __init__(self, config_data):
        """
        params:
            config_data: data used to configure the zoom api client
        """
        # set api client specific vars
        self.config_data = config_data

        # initialize module classes
        self.users = users.Users(self)
        self.group = group.Group(self)
        self.report = report.Report(self)
        self.dashboard = dashboard.Dashboard(self)

        # initialize user model
        self.model = {"users": None}

    def generate_jwt(self):
        """Generate valid jwt token for use in Zoom API requests"""
        headers = {
            "alg": "HS256",
            "typ": "JWT",
        }

        encoded = jwt.encode(
            {
                "iss": self.config_data["api_key"],
                "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=30),
            },
            self.config_data["api_secret"],
            algorithm="HS256",
            headers=headers,
        )

        return {
            "Authorization": f"Bearer {encoded}",
            "Content-type": "application/json",
        }

    def do_request(self, request_type, resource, request_parameters, body=None):
        """Perform API request using the specified parameters"""
        if request_type == "get":
            rsp = requests.get(
                self.config_data["root_request_url"] + resource,
                params=request_parameters,
                headers=self.generate_jwt(),
                verify=True,
            )

        elif request_type == "delete":
            rsp = requests.delete(
                self.config_data["root_request_url"] + resource,
                params=request_parameters,
                headers=self.generate_jwt(),
                verify=True,
            )

        elif request_type == "patch":
            rsp = requests.patch(
                self.config_data["root_request_url"] + resource,
                params=request_parameters,
                data=body,
                headers=self.generate_jwt(),
                verify=True,
            )

        elif request_type == "post":
            rsp = requests.post(
                self.config_data["root_request_url"] + resource,
                params=request_parameters,
                data=body,
                headers=self.generate_jwt(),
                verify=True,
            )

        if "Retry-After" in rsp.headers.keys():
            logging.warning("Retry-After detected: %s", rsp.headers["Retry-After"])
            logging.warning("X-RateLimit-Limit: %s", rsp.headers["X-RateLimit-Limit"])
            logging.warning(
                "X-RateLimit-Remaining: %s", rsp.headers["X-RateLimit-Remaining"]
            )

        try:
            result = rsp.json()
        except RequestException:
            result = rsp

        rsp.close()

        return result
