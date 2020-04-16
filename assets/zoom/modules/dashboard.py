import logging
from time import sleep
from datetime import datetime, timedelta


class dashboard:
    def __init__(self, controller, *args, **kwargs):
        self.zoom = controller

    def get_past_meetings(self, from_date, to_date):
        """
        Finds Zoom meetings in provided date range. Note only one request per minute may be made due to Zoom rate limits.

        params:
            from_date: date to begin search for meetings in format ("%Y-%m-%d")
            to_date: date to end search for meetings in format ("%Y-%m-%d")

        returns:
            list of dictionaries containing relevant meeting information from Zoom.
        """

        more_pages = True
        next_page_token = ""
        result_list = []

        while more_pages:
            result = self.zoom.api_client.do_request(
                "get",
                "metrics/meetings",
                {
                    "from": from_date,
                    "to": to_date,
                    "type": "past",
                    "page_size": 200,
                    "next_page_token": next_page_token,
                },
            )

            result_list += result["meetings"]
            sleep(60)
            if result["next_page_token"] != "":
                next_page_token = result["next_page_token"]
            else:
                break

        return result_list

    def get_past_meeting_participants(self, meeting_uuid):
        """
        Finds Zoom meeting participants from given meeting_uuid (specific instance of Zoom meeting).
        Note only one request per second may be made due to Zoom rate limits.

        params:
            meeting_uuid: meeting uuid which you'd like to find participants for

        returns:
            list of dictionaries containing relevant meeting information from Zoom.
        """

        more_pages = True
        next_page_token = ""
        result_list = []

        while more_pages:
            result = self.zoom.api_client.do_request(
                "get",
                "metrics/meetings/" + meeting_uuid + "/participants",
                {"type": "past", "page_size": 200, "next_page_token": next_page_token},
            )

            sleep(1)

            if "participants" in result.keys():
                result_list += result["participants"]
            else:
                result_list += [
                    {"error_code": result["code"], "error": result["message"]}
                ]
                break

            if result["next_page_token"] != "":
                next_page_token = result["next_page_token"]
            else:
                break

        return result_list
