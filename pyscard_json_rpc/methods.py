import binascii
import struct
import uuid
from uuid import UUID

import smartcard.System
from smartcard.CardConnection import CardConnection
from smartcard.reader.Reader import Reader

from pyscard_json_rpc import connections


async def smartcard_get_readers(websocket, **params):
    return {"readers": [reader.name for reader in smartcard.System.readers()]}


async def smartcard_connect(websocket, **params):
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


async def connection_get_atr(websocket, **params):
    connection_id = UUID(params["connection_id"])
    connection: CardConnection = connections.card_connections[websocket.scope["client"]][connection_id]

    atr = connection.getATR()

    return {
        "atr": binascii.hexlify(bytes(atr)).decode("utf-8"),
    }


async def connection_transmit(websocket, **params):
    connection_id = UUID(params["connection_id"])
    connection: CardConnection = connections.card_connections[websocket.scope["client"]][connection_id]

    apdu_request = binascii.unhexlify(params["apdu"])
    data, sw1, sw2 = connection.transmit(
        bytes=[int(x) for x in apdu_request or []],
        protocol=params.get("protocol"),
    )

    return {
        "data": binascii.hexlify(bytes(data)).decode("utf-8"),
        "sw1": binascii.hexlify(struct.pack("<B", sw1)).decode("utf-8"),
        "sw2": binascii.hexlify(struct.pack("<B", sw2)).decode("utf-8"),
    }


async def connection_disconnect(websocket, **params):
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
