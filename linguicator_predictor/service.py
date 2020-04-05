import json
import logging
import linguicator_predictor


async def handle_request(websocket, request_data):
    """
    I handle a request passing the received data to the proper handler.

    :param websocket: websocket object representing the connection
    :type  websocket: websockets.server.WebSocketServerProtocol

    :param request_data: the received request data
    :type  request_data: str

    :returns: nothing
    :rtype: None
    """
    # define request handlers
    request_handlers = {
        '/predict': handle_prediction_request,
    }

    # convert request json to dictionary
    request_dict = json.loads(request_data)

    # handle the request
    await request_handlers[request_dict['resource']](websocket,
                                                     request_dict['id'],
                                                     request_dict['data'])


def predict(text, length):
    """
    I make a prediction of how a text could continue.

    :param text: the text I will make the prediction on
    :type  text: str

    :param length: the maximum length of the prediction in characters
    :type  length: int

    :returns: the predicted text
    :rtype: str
    """
    prediction = linguicator_predictor.model.predict(text, length)

    # remove the original text from the prediction
    prediction = prediction[len(text):]

    # remove everything after last ' ' and return
    return ' '.join(prediction.split()[:-1])


async def handle_prediction_request(websocket, request_id, request_data):
    """
    I handle a request to make a prediction on a given piece of text.

    :param websocket: websocket object representing the connection
    :type  websocket: websockets.server.WebSocketServerProtocol

    :param request_id: the id of the request being handled
    :type  request_id: int

    :param request_data: data from the request
    :type  request_data: dict[str, any]

    :returns: nothing
    :rtype: None
    """
    response_data = {
        'id': request_id,
        'code': 200,
        'data': predict(request_data['text'], request_data['length'])
    }
    logging.info('Sending data through websocket connection')
    logging.debug(f'Sending: {response_data}')
    await websocket.send(json.dumps(response_data, ensure_ascii = False))
