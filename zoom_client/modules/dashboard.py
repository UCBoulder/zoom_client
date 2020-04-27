import logging
from time import sleep
from datetime import datetime, timedelta
from ratelimit import limits, sleep_and_retry


class dashboard:
    def __init__(self, controller, *args, **kwargs):
        self.zoom = controller

    def get_past_meetings(self, from_date: str, to_date: str) -> list:
        """
        Finds Zoom meetings in provided date range. Note only one request per minute may be made due to Zoom rate limits.

        params:
            from_date: date to begin search for meetings in format ("%Y-%m-%d")
            to_date: date to end search for meetings in format ("%Y-%m-%d")

        returns:
            list of dictionaries containing relevant meeting information from Zoom.
        """
        logging.info("Gathering Zoom meetings data...")
        # Note: artificial rate limit
        # more detail can be found here: https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits
        @sleep_and_retry
        @limits(calls=19, period=65)
        def make_requests(
            page_number: int = 1, next_page_token: str = None, result_list: list = []
        ) -> list:

            logging.info("Making meeting request " + str(page_number))

            result = self.zoom.api_client.do_request(
                "get",
                "metrics/meetings",
                {
                    "from": from_date,
                    "to": to_date,
                    "type": "past",
                    "page_size": 300,
                    "next_page_token": next_page_token,
                },
            )

            page_number += 1

            if "meetings" in result.keys():
                result_list += result["meetings"]
            else:
                result_list += [
                    {"error_code": result["code"], "error": result["message"]}
                ]

            if "code" in result.keys():
                logging.error(
                    "Error: " + str(result["code"]) + " " + str(result["message"])
                )
                return result_list

            elif "next_page_token" in result.keys():

                if result["next_page_token"] != "":
                    make_requests(
                        page_number=page_number,
                        next_page_token=result["next_page_token"],
                        result_list=result_list,
                    )
                    return result_list
                else:
                    return result_list

        result_list = make_requests()

        return result_list

    def get_past_meeting_participants(self, meeting_uuid: str) -> list:
        """
        Finds Zoom meeting participants from given meeting_uuid (specific instance of Zoom meeting).
        Note only one request per second may be made due to Zoom rate limits.

        params:
            meeting_uuid: meeting uuid which you'd like to find participants for

        returns:
            list of dictionaries containing relevant meeting information from Zoom.
        """

        logging.info("Gathering Zoom meeting participant data...")
        # Note: artificial rate limit
        # more detail can be found here: https://marketplace.zoom.us/docs/api-reference/rate-limits#rate-limits
        @sleep_and_retry
        @limits(calls=39, period=5)
        def make_requests(
            page_number: int = 1, next_page_token: str = None, result_list: list = []
        ) -> list:
            logging.info("Making meeting partcipants request " + str(page_number))

            result = self.zoom.api_client.do_request(
                "get",
                "metrics/meetings/" + meeting_uuid + "/participants",
                {"type": "past", "page_size": 300, "next_page_token": next_page_token},
            )

            page_number += 1

            if "participants" in result.keys():
                result_list += result["participants"]
            else:
                result_list += [
                    {"error_code": result["code"], "error": result["message"]}
                ]

            if "code" in result.keys():
                logging.error(
                    "Error: " + str(result["code"]) + " " + str(result["message"])
                )
                return result_list

            elif "next_page_token" in result.keys():
                if result["next_page_token"] != "":
                    make_requests(
                        page_number=page_number,
                        next_page_token=result["next_page_token"],
                        result_list=result_list,
                    )
                    return result_list
                else:
                    return result_list

        result_list = make_requests()

        return result_list
