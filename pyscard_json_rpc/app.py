import logging
from collections import defaultdict
from typing import Dict
from uuid import UUID

from fastapi import FastAPI
from smartcard.CardConnection import CardConnection
from smartcard.Exceptions import SmartcardException
from starlette.websockets import WebSocket, WebSocketDisconnect

from pyscard_json_rpc import connections
from pyscard_json_rpc.json_rpc import format_error, get_message_type, format_response
from pyscard_json_rpc.methods import METHOD_HANDLERS

logger = logging.getLogger(__name__)


def environment_setup():
    pass


def logging_setup():
    # logging.basicConfig(level=logging.INFO)
    # logger.setLevel(logging.INFO)
    pass


app = FastAPI(on_startup=[environment_setup, logging_setup], on_shutdown=[])


### tachocard app -> smartcard service
# smartcard.get_readers
# smartcard.get_cards
# smartcard.connect
# smartcard.get_atr
# smartcard.get_apdu
# smartcard.disconnect

### smartcard service -> tachocard app
# observer.reader_added
# observer.reader_removed
# observer.card_added
# observer.card_removed


@app.websocket("/ws/pyscard-json-rpc")
async def websocket_handler(websocket: WebSocket):

    await websocket.accept()

    try:
        while True:
            message = await websocket.receive_json()
            message_type = get_message_type(message)

            if message_type == "request":
                if message["method"] in METHOD_HANDLERS:
                    try:
                        result = await METHOD_HANDLERS[message["method"]](
                            websocket=websocket, **message.get("params", {})
                        )
                        response = format_response(result=result, request_id=message.get("id"))
                    except (KeyError, StopIteration) as exc:
                        logger.exception(f"caught exception during handling {message['method']}", exc_info=exc)
                        response = format_error(code=-32602, request_id=message.get("id"))
                    except SmartcardException as exc:
                        logger.exception(f"caught exception during handling {message['method']}", exc_info=exc)
                        response = format_error(code=-32000, message=exc.args[0], request_id=message.get("id"))
                else:
                    response = format_error(code=-32601, request_id=message.get("id"))

                await websocket.send_json(response)
            elif message_type in {"success", "error"}:
                pass

    except ValueError as exc:
        logger.exception(exc)
        await websocket.close(code=1003)
    except WebSocketDisconnect:
        pass
    finally:
        connection_id: UUID
        connection: CardConnection
        for connection_id, connection in connections.card_connections[websocket.scope["client"]].items():
            logger.error(f"connection {connection_id} was left open")
            connection.disconnect()
