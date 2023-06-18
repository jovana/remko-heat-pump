import requests
import logging
from .const import BASE_API_URL

_LOGGER = logging.getLogger(__name__)


class RemkoHeatpump():
    pass

    def __init__(self) -> None:
        """Initialize the class."""
        self._url = f"{BASE_API_URL}/cgi-bin/webapi.cgi"

    def api_request(self, query_value: int):
        """
        Getting values from API.
        Check the readme.md for available codes.

        Args:
            query_value (int): _description_

        Returns:
            _type_: _description_
        """
        _LOGGER.debug(
            f"Getting value: {str(query_value)} from heatpump API.")

        # Getting values from API
        payload = {
            "SMT_ID": "0000000000000000",
            "query_list": [query_value]
        }

        response = requests.post(self._url, json=payload)
        if response.status_code == 200:
            json_response = response.json()
            _LOGGER.debug(json_response)
            if 'values' in json_response:
                return json_response['values'][str(query_value)]

        return 0
