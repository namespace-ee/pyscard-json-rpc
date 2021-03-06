import asyncio
import logging
from collections import defaultdict
from typing import Dict
from uuid import UUID

from fastapi import FastAPI
from smartcard.CardConnection import CardConnection
from smartcard.CardMonitoring import CardMonitor
from smartcard.Exceptions import SmartcardException
from smartcard.ReaderMonitoring import ReaderMonitor
from starlette.websockets import WebSocket, WebSocketDisconnect

from pyscard_json_rpc import connections
from pyscard_json_rpc.json_rpc import format_error, get_message_type, format_response
from pyscard_json_rpc.methods import METHOD_HANDLERS
from pyscard_json_rpc.observers import PrintReaderObserver, PrintCardObserver

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
    # define monitors/observers
    loop = asyncio.get_event_loop()
    readermonitor = ReaderMonitor()
    readerobserver = PrintReaderObserver(websocket=websocket, loop=loop)
    cardmonitor = CardMonitor()
    cardobserver = PrintCardObserver(websocket=websocket, loop=loop)

    try:
        # add observers
        readermonitor.addObserver(readerobserver)
        cardmonitor.addObserver(cardobserver)
        while True:
            message = await websocket.receive_json()
            message_type = get_message_type(message)

            if message_type == "request":
                if message["method"] in METHOD_HANDLERS:
                    try:
                        result = METHOD_HANDLERS[message["method"]](websocket=websocket, **message.get("params", {}))
                        response = format_response(result=result, request_id=message.get("id"))
                    except (KeyError, ValueError, TypeError, StopIteration) as exc:
                        logger.exception(f"caught exception during handling {message['method']}", exc_info=exc)
                        response = format_error(code=-32602, message=str(exc.args[0]), request_id=message.get("id"))
                    except SmartcardException as exc:
                        logger.exception(f"caught exception during handling {message['method']}", exc_info=exc)
                        response = format_error(code=-32000, message=str(exc.args[0]), request_id=message.get("id"))
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

        try:
            # This can fail if the observer was not added to the monitor.
            readermonitor.deleteObserver(readerobserver)
        finally:
            # note: remove card observer even if reader observer delete fails!
            cardmonitor.deleteObserver(cardobserver)
