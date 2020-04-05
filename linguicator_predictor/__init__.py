import asyncio
import websockets
import logging

from linguicator_predictor.websocket import handle_websocket_connection
from linguicator_predictor.models.en.distilgpt2 import DistilGPT2

PORT = 8765
HOST = 'localhost'
LOGGING_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
LOGGING_DATE_FORMAT = '%m/%d/%Y %I:%M:%S %p'


def main():
    """
    I start the server.

    :returns: nothing
    :rtype: None
    """
    # configure predictor
    global model
    model = DistilGPT2()

    # configure logger
    logging.basicConfig(format=LOGGING_FORMAT,
                        datefmt=LOGGING_DATE_FORMAT,
                        level=logging.INFO)

    # start server
    logging.info('Starting server...')
    start_server = websockets.serve(handle_websocket_connection,
                                    HOST,
                                    PORT)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
