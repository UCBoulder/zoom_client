"""
Zoom client class which assists with performing work using Zoom API
"""

import datetime
import json
import logging
import sys

import jwt
import requests

import zoom_client.modules.dashboard as dashboard
import zoom_client.modules.group as group
import zoom_client.modules.report as report
import zoom_client.modules.users as users

# set recursion limit higher for rate limitations functions
sys.setrecursionlimit(20000)
requests.packages.urllib3.disable_warnings()


class Client:
    """ Zoom client class which assists with performing work using Zoom API """

    def __init__(self, config_data):
        """
        params:
            config_data: data used to configure the zoom api client
        """
        # set api client specific vars
        self.root_request_url = config_data["root_request_url"]
        self.key = config_data["api_key"]
        self.secret = config_data["api_secret"]
        self.data_type = config_data["data_type"]

        # initialize module classes
        self.users = users.Users(self)
        self.group = group.Group(self)
        self.report = report.Report(self)
        self.dashboard = dashboard.Dashboard(self)

        # initialize user model
        self.model = {"users": None}

    def generate_jwt(self):
        """ Generate valid jwt token for use in Zoom API requests """
        headers = {
            "alg": "HS256",
            "typ": "JWT",
        }

        encoded = jwt.encode(
            {
                "iss": self.key,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=30),
            },
            self.secret,
            algorithm="HS256",
            headers=headers,
        )

        return {
            "Authorization": "Bearer " + encoded.decode("utf-8"),
            "Content-type": "application/json",
        }

    def do_request(self, request_type, resource, request_parameters, body={}):

        if request_type == "get":
            rsp = requests.get(
                self.root_request_url + resource,
                params=request_parameters,
                headers=self.generate_jwt(),
                verify=True,
            )

        elif request_type == "delete":
            rsp = requests.delete(
                self.root_request_url + resource,
                params=request_parameters,
                headers=self.generate_jwt(),
                verify=True,
            )

        elif request_type == "patch":
            rsp = requests.patch(
                self.root_request_url + resource,
                params=request_parameters,
                data=body,
                headers=self.generate_jwt(),
                verify=True,
            )

        elif request_type == "post":
            rsp = requests.post(
                self.root_request_url + resource,
                params=request_parameters,
                data=body,
                headers=self.generate_jwt(),
                verify=True,
            )

        if "Retry-After" in rsp.headers.keys():
            logging.warning("Retry-After detected: " + str(rsp.headers["Retry-After"]))
            logging.warning(
                "X-RateLimit-Limit: " + str(rsp.headers["X-RateLimit-Limit"])
            )
            logging.warning(
                "X-RateLimit-Remaining: " + str(rsp.headers["X-RateLimit-Remaining"])
            )

        try:
            result = rsp.json()
        except:
            result = rsp

        rsp.close()

        return result
