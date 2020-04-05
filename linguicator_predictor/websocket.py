import logging
import websockets

from linguicator_predictor.service import handle_request


async def handle_websocket_connection(websocket, path):
    """
    I handle a new websocket connection by listening to requests and handling
    the received data until the connection is closed.

    :param websocket: websocket object representing the connection
    :type  websocket: websockets.server.WebSocketServerProtocol

    :param path: the connection relative path
    :type  path: str

    :returns: nothing
    :rtype: None
    """
    logging.info('New connection established')

    # wait for user requests until the connection is closed
    while True:

        # handle request
        try:
            await wait_for_user_request(websocket)

        # connection closed successfully: log it and return
        except websockets.exceptions.ConnectionClosedOK:
            logging.info('Connection closed cleanly')
            return

        # unexpected error: log it and return
        except Exception as e:
            logging.info(f'Connection closed due unexpected error: {e}')
            return


async def wait_for_user_request(websocket):
    """
    I wait for data in the websocket connection.

    :param websocket: websocket object representing the connection
    :type  websocket: websockets.server.WebSocketServerProtocol

    :returns: nothing
    :rtype: None
    """
    # wait for a new request
    request = await websocket.recv()

    # log the received request
    logging.info('Data received through websocket connection')
    logging.debug(f'Received: "{request}"')

    # handle the request
    await handle_request(websocket, request)
