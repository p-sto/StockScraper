"""File contains definition of HTTP clients """
from datetime import datetime
from urllib.parse import urljoin
from typing import Any, Callable, List, Dict, Optional

import logging
import requests
from requests.models import Response
from StockScraper.Generic.exceptions import HTTPError


REST_API_METHODS = ['POST', 'GET', 'PUT', 'PATCH', 'DELETE']


def validate_response(called_method: Callable) -> Callable:
    """Decorator for HTTPClient validating received response for REST API methods.
    If status code from server is different than 200 raises HTTPError.

    :param called_method: requests methods - POST, GET, PUT, PATH, DELETE
    :return: response from server
    """
    def wrapper(method: Callable, endpoint: str, *args: List[Any], **kwargs: Dict[Any, Any]) -> Response:
        """Executes decorated function and checks status_code."""
        resp = called_method(method, endpoint, *args, **kwargs)
        if resp.status_code != 200:
            logging.error('HTTP Client returned status code %s for url %s', resp.status_code, resp.url)
            raise HTTPError('HTTP Client returned status code {0} for url {1}'.format(str(resp.status_code), resp.url))
        return resp
    return wrapper


class HTTPClient:
    """Definition of HTTP client. """

    def __init__(self, host_name: str) -> None:
        """Initialize object.

        :param host_name: string containing host name
        :return: None
        """
        self.host_name = host_name

    def __repr__(self) -> str:
        """Return nicer print presentation."""
        return '{} - {}'.format(self.__class__.__name__, self.host_name)

    @validate_response
    def call_endpoint(self, method: str, endpoint: str, *args: List[Any], **kwargs: Dict[Any, Any]) -> Response:
        """Call api endpoint method.

        :param method: REST API methods name (string) - 'POST', 'GET', 'PUT', 'PATCH', 'DELETE'
        :param endpoint: endpoint which will be called with method.
        :param args: additional arguments
        :param kwargs: additional key-worded arguments
        :return:
        """
        logging.info('Calling method %s for endpoint %s', method, endpoint)

        if method.upper() not in REST_API_METHODS:
            logging.error('Method %s does not match REST API METHODS: %s', method, ','.join(REST_API_METHODS))
            raise TypeError('Method {0} does not match REST API METHODS: {1}'.format(str(method),
                                                                                     ','.join(REST_API_METHODS)))

        req_method = getattr(requests, method.lower())
        resp = req_method(urljoin(self.host_name, endpoint), *args, **kwargs)
        return resp

    @staticmethod
    def create_endpoint_url(symbol: str,
                            date_from: Optional[datetime] = None,
                            date_to: Optional[datetime] = None,
                            days: Optional[int] = None) -> None:
        """Abstract method for creating endpoint url."""
        raise NotImplementedError


class JSONClient:   # pylint: disable=too-few-public-methods
    """Mixin for JSON client."""
    @staticmethod
    def to_json(response: Response) -> dict:
        """Convert response from requests to json object.

        :param response: response from requests
        :return: json object
        """
        return response.json()
