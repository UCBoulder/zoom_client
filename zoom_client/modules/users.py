"""
zoom_client class and related methods for gathering data about or
changing properties of existing Zoom users
"""
import json
import logging
import time
from datetime import datetime

from ratelimit import limits, sleep_and_retry


class Users:
    """
    zoom_client users class for gathering data about or
    changing properties of existing Zoom users
    """

    def __init__(self, client):
        self.zoom = client

    def update_user(self, user_id, update_properties=json.dumps({})):
        """Update single Zoom user property by userid"""
        logging.info(
            "Updating user with ID: "
            + user_id
            + " with properties: "
            + update_properties
        )

        result = self.zoom.do_request(
            "patch", "users/" + user_id, "", body=update_properties
        )

        return result

    def batch_update_users(self, user_list, update_properties=json.dumps({})):
        """Update Zoom user properties in batch using provided list of userid's"""
        number_users_updated = 0
        time_interval_request_count = 0
        start_time_interval = datetime.now()

        for user_id in user_list:
            resp = self.update_user(user_id, update_properties)
            time_interval_request_count += 1

            if resp.status_code == 204:
                logging.info("Updated user %s successfully.", user_id)
                number_users_updated += 1

            # update the current time interval to accoutn for time restrictions in Zoom API
            cur_time_interval = datetime.now()

            # Check to see if less than a second has passed and 10 requests have already been made
            # If so, sleep for the remaining time until the next second begins
            if (
                cur_time_interval - start_time_interval
            ).seconds < 1 and time_interval_request_count == 10:
                logging.info(
                    "Waiting to ensure Zoom request time restrictions are met."
                )
                time.sleep(
                    (1 / 1000000)
                    * (
                        1000000
                        - (cur_time_interval - start_time_interval).microseconds
                        + 1000
                    )
                )
                start_time_interval = datetime.now()
                time_interval_request_count = 1

            # Else, if greater than a second has passed reset values to begin time
            # restriction counts again.
            elif (cur_time_interval - start_time_interval).seconds >= 1:
                start_time_interval = datetime.now()
                time_interval_request_count = 1

        return number_users_updated

    def delete_user(self, user_id):
        """Delete single Zoom user by userid"""
        logging.info("Deleting user with ID: %s", user_id)

        result = self.zoom.do_request(
            "delete", "users/" + user_id, {"action": "delete"}
        )

        return result

    def batch_delete_users(self, user_list):
        """Delete Zoom users in batch based on provided list of userid's"""
        number_users_deprovisioned = 0
        time_interval_request_count = 0
        start_time_interval = datetime.now()

        for user_id in user_list:

            resp = self.delete_user(user_id)
            time_interval_request_count += 1

            if resp.status_code == 204:
                logging.info("Deprovisioned user %s successfully.", user_id)
                number_users_deprovisioned += 1

            # update the current time interval to accoutn for time restrictions in Zoom API
            cur_time_interval = datetime.now()

            # Check to see if less than a second has passed and 10 requests have already been made
            # If so, sleep for the remaining time until the next second begins
            if (
                cur_time_interval - start_time_interval
            ).seconds < 1 and time_interval_request_count == 10:
                logging.info(
                    "Waiting to ensure Zoom request time restrictions are met."
                )
                time.sleep(
                    (1 / 1000000)
                    * (
                        1000000
                        - (cur_time_interval - start_time_interval).microseconds
                        + 1000
                    )
                )
                start_time_interval = datetime.now()
                time_interval_request_count = 1

            # Else, if greater than a second has passed reset values to begin time
            # restriction counts again.
            elif (cur_time_interval - start_time_interval).seconds >= 1:
                start_time_interval = datetime.now()
                time_interval_request_count = 1

        return number_users_deprovisioned

    def get_current_users(self):
        """Gather current Zoom user data from account"""
        logging.info("Gathering current Zoom user data ...")

        # Note: artificial rate limit
        # more detail can be found here:
        # https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits
        @sleep_and_retry
        @limits(calls=60, period=5)
        def make_requests(
            page_number: int = 1, page_count: int = None, result_list: list = None
        ) -> list:

            logging.info("Making user request %s of %s", page_number, page_count)
            # make the Zoom api request and parse the result for the data we need
            result = self.zoom.do_request(
                "get", "users", {"page_size": "300", "page_number": page_number}
            )

            # if no users are returned in the result, we break our loop
            if "users" in result:
                user_results = result["users"]
                result_list += user_results

            page_number += 1

            if page_number <= int(result["page_count"]):
                make_requests(
                    page_number=page_number,
                    page_count=result["page_count"],
                    result_list=result_list,
                )

            return result_list

        users_listing = make_requests()

        self.zoom.model["users"] = users_listing

        return users_listing

    def get_users_from_list(self, user_list):
        """Gather user data based on list of Zoom userid's provided"""
        logging.info("Gathering current Zoom user data from list...")

        result_list = []
        for user in user_list:
            result = self.zoom.client.do_request(
                "get", "users/" + user, {"userId": user}
            )
            result_list.append(result)

        self.zoom.model["users"] = result_list

        return result_list

    def get_current_user_type_counts(self):
        """Gather current user type counts from Zoom account"""
        logging.info("Gathering current Zoom user metrics...")

        # create various counts which will help provide metrics
        pro_account_count = 0
        basic_account_count = 0
        corp_account_count = 0
        account_count = 0

        account_count = len(self.zoom.model["users"])

        for user_data in self.zoom.model["users"]:

            # change type from integer to human-readable value
            # also make counts of the number of accounts per type
            if user_data["type"] == 1:
                basic_account_count += 1
                user_data["type"] = "Basic"
            elif user_data["type"] == 2:
                pro_account_count += 1
                user_data["type"] = "Pro"
            elif user_data["type"] == 3:
                corp_account_count += 1
                user_data["type"] = "Corp"

        # Share various metrics with the user on
        # total, basic, pro and deprovisioning information to better
        # inform them before proceeding.
        logging.info("Total accounts: %s", account_count)
        logging.info("Basic accounts: %s", basic_account_count)
        logging.info("Pro accounts: %s", pro_account_count)
        logging.info("Corp accounts: %s", corp_account_count)

        return {
            "Basic Accounts": basic_account_count,
            "Pro Accounts": pro_account_count,
            "Corp Accounts": corp_account_count,
            "Total Accounts": account_count,
        }
