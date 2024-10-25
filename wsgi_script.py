"""WSGI script for running the application."""

import logging
import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from src.main import app as application


class LoggingMiddleware:
    """Middleware class for logging incoming requests and outgoing responses."""

    def __init__(self, app_handler):
        """
        Initialize the LoggingMiddleware.

        Parameters:
        - app_handler (callable): The application handler.
        """
        self.__application = app_handler

    def __call__(self, environ, start_response):
        """
        Call method to handle the request.

        Parameters:
        - environ (dict): The WSGI environment.
        - start_response (callable): The WSGI start_response function.

        Returns:
        - result: The response generated by the application.
        """
        request_method = environ["REQUEST_METHOD"]
        path_info = environ["PATH_INFO"]
        query_string = environ.get("QUERY_STRING", "")

        if query_string:
            path_info += f"?{query_string}"

        logger.debug("Incoming request: %s %s", request_method, path_info)

        def _start_response(status, headers, *args):
            """
            Custom start_response function to log response status.

            Parameters:
            - status (str): The HTTP status code.
            - headers (list): List of response headers.
            - *args: Additional arguments.

            Returns:
            - result: The result of start_response function.
            """
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            remote_addr = environ.get("REMOTE_ADDR", "-")
            server_protocol = environ.get("SERVER_PROTOCOL", "-")
            log_msg = (
                f'- - {remote_addr} - - [{timestamp}] "{request_method} {path_info} '
                f'{server_protocol}" {status} -'
            )
            logger.info(log_msg)
            return start_response(status, headers, *args)

        return self.__application(environ, _start_response)


application = LoggingMiddleware(application)
