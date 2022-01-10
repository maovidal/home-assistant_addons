"""
This script listens to logs provided by clients via UDP on the configured port

When a pattern matches the content of the received log, a post request is made
to the Home Assistant API.


Mauricio Vidal, 2022
https://github.com/MrMauro/home-assistant_addons

The part related to the "Syslog Server" is based on:
https://gist.github.com/marcelom/4218010

"""

import logging
import socketserver
import os
from requests import post
from config import (
    DEBUG_MODE,
    CUSTOM_PORT,
    ENDPOINT_1,
    ENDPOINT_2,
    TO_SEEK_1,
    TO_SEEK_2,
    PAYLOAD_1,
    PAYLOAD_2,
)


# Server address
CUSTOM_HOST = '0.0.0.0'


# Request header using the Home Assistant Token.
headers = {
    'Authorization': 'Bearer ' + os.environ.get('SUPERVISOR_TOKEN'),
    'content-type': 'application/json',
}


# URLs for the endpoints
endpoint_1_url = 'http://supervisor/core/api/' + ENDPOINT_1
endpoint_2_url = 'http://supervisor/core/api/' + ENDPOINT_2


# Own logger setup (This is not related to the Syslog server)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger_sl2ha = logging.getLogger(__name__)

# Greet
logger_sl2ha.info("Syslog to Home Assistant has started using the following configuration:\n\tDebug: %s|%s\n\tPort: %s|%s\n\tEndpoint 1: %s|%s\n\tEndpoint 2: %s|%s\n\tSeek 1: %s|%s\n\tSeek 2: %s|%s\n\tPayload 1: %s|%s\n\tPayload 2: %s|%s", type(DEBUG_MODE), DEBUG_MODE, type(CUSTOM_PORT), CUSTOM_PORT, type(endpoint_1_url), endpoint_1_url, type(endpoint_2_url), endpoint_2_url, type(TO_SEEK_1), TO_SEEK_1, type(TO_SEEK_2), TO_SEEK_2, type(PAYLOAD_1), PAYLOAD_1, type(PAYLOAD_2), PAYLOAD_2)


# Own-logger level setup
if str(DEBUG_MODE) == 'true' or str(DEBUG_MODE) == 'True' :
    logger_sl2ha.setLevel(logging.DEBUG)
    logger_sl2ha.info("Debug mode has been enabled")
else:
    logger_sl2ha.setLevel(logging.INFO)
    logger_sl2ha.info("Debug mode has been disabled")


class SyslogUDPHandler(socketserver.BaseRequestHandler):
    """
    This is an extension of the class to implement a handler.
    """
    def handle(self):
        """
        On every log received, the content will be inspected to check the
        existence of certain text. When it matches, a post request is made to
        the configured Home Assistance API url using the pertinent payload.
        """
        # The data is received.
        data = bytes.decode(self.request[0].strip())

        # Socket is not implemented.
        # socket = self.request[1]

        # This is the address of the device that provided the log
        source = self.client_address[0]

        # Every case of text to match is evaluated
        logger_sl2ha.debug("%s has a new log with data:\n%s", source, str(data))

        if TO_SEEK_1 in str(data):
            logger_sl2ha.info("%s: has the content: %s", source, TO_SEEK_1)
            response = post(url=endpoint_1_url, headers=headers, data=PAYLOAD_1)
            logger_sl2ha.debug("Response from API at: %s with code: %s, data: %s", endpoint_1_url, str(response), str(response.text))

        elif TO_SEEK_2 in str(data):
            logger_sl2ha.info("%s: has the content: %s", source, TO_SEEK_2)
            response = post(url=endpoint_2_url, headers=headers, data=PAYLOAD_2)
            logger_sl2ha.debug("Response from API at: %s with code: %s, data: %s", endpoint_2_url, str(response), str(response.text))


if __name__ == "__main__":
    try:
        server = socketserver.UDPServer(
            server_address=(CUSTOM_HOST,CUSTOM_PORT),
            RequestHandlerClass=SyslogUDPHandler,
        )
        server.serve_forever(
            poll_interval=0.5
        )
    except (IOError, SystemExit):
        raise
    except KeyboardInterrupt:
        print ("Crtl+C Pressed. Shutting down.")
