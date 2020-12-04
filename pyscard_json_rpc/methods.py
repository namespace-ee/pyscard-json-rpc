import uuid
from uuid import UUID

import smartcard.System
from smartcard.CardConnection import CardConnection
from smartcard.reader.Reader import Reader
from smartcard.util import toBytes, toHexString, PACK

from pyscard_json_rpc import connections


def smartcard_get_readers(websocket, **params):
    return {"readers": [reader.name for reader in smartcard.System.readers()]}


def smartcard_connect(websocket, **params):
    readers = smartcard.System.readers()
    reader: Reader = next(reader for reader in readers if reader.name == params.get("reader"))

    connection_id: UUID = uuid.uuid4()
    connection: CardConnection = reader.createConnection()
    connections.card_connections[websocket.scope["client"]][connection_id] = connection

    connection.connect(
        protocol=params.get("protocol"),
        mode=params.get("mode"),
        disposition=params.get("disposition"),
    )

    return {
        "connection_id": str(connection_id),
    }


def connection_get_atr(websocket, **params):
    connection_id = UUID(params["connection_id"])
    connection: CardConnection = connections.card_connections[websocket.scope["client"]][connection_id]

    atr = connection.getATR()

    return {
        "atr": toHexString(atr, PACK),
    }


def connection_transmit(websocket, **params):
    connection_id = UUID(params["connection_id"])
    connection: CardConnection = connections.card_connections[websocket.scope["client"]][connection_id]

    data, sw1, sw2 = connection.transmit(
        bytes=toBytes(params["apdu"]),
        protocol=params.get("protocol"),
    )

    return {
        "data": toHexString(data, PACK),
        "sw1": toHexString([sw1], PACK),
        "sw2": toHexString([sw2], PACK),
    }


def connection_disconnect(websocket, **params):
    connection_id = UUID(params["connection_id"])
    connection: CardConnection = connections.card_connections[websocket.scope["client"]][connection_id]
    connection.disconnect()

    del connections.card_connections[websocket.scope["client"]][connection_id]

    return {}


METHOD_HANDLERS = {
    "smartcard.get_readers": smartcard_get_readers,
    "smartcard.connect": smartcard_connect,
    "connection.get_atr": connection_get_atr,
    "connection.transmit": connection_transmit,
    "connection.disconnect": connection_disconnect,
}
