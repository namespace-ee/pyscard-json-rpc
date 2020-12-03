from __future__ import print_function

import asyncio
import uuid

from smartcard.ATR import ATR
from smartcard.util import toHexString, PACK
from smartcard.CardMonitoring import CardObserver
from smartcard.ReaderMonitoring import ReaderObserver

from pyscard_json_rpc.json_rpc import format_request

PROTOCOLS_MAPPING = {
    "T=0": 0x00000001,  # T0_protocol
    "T=1": 0x00000002,  # T1_protocol
    "T=15": 0x00000008,  # T15_protocol
}


class PrintReaderObserver(ReaderObserver):
    """A simple reader observer that is notified
    when readers are added/removed from the system and
    prints the list of readers
    """

    websocket = None
    loop = None

    def __init__(self, websocket, loop):
        super().__init__()
        self.websocket = websocket
        self.loop = loop

    def update(self, observable, actions):
        addedreaders, removedreaders = actions
        for reader in addedreaders or []:
            response = format_request(
                method="observer.reader_added",
                request_id=str(uuid.uuid4()),
                params={"reader": reader.name},
            )
            asyncio.run_coroutine_threadsafe(self.websocket.send_json(response), self.loop)

        for reader in removedreaders or []:
            response = format_request(
                method="observer.reader_removed",
                request_id=str(uuid.uuid4()),
                params={"reader": reader.name},
            )
            asyncio.run_coroutine_threadsafe(self.websocket.send_json(response), self.loop)


class PrintCardObserver(CardObserver):
    """A simple card observer that is notified
    when cards are inserted/removed from the system and
    prints the list of cards
    """

    websocket = None
    loop = None

    def __init__(self, websocket, loop):
        super().__init__()
        self.websocket = websocket
        self.loop = loop

    def update(self, observable, actions):
        addedcards, removedcards = actions
        for card in addedcards:
            atr = ATR(card.atr)
            response = format_request(
                method="observer.card_added",
                request_id=str(uuid.uuid4()),
                params={
                    "reader": str(card.reader),
                    "atr": toHexString(card.atr, PACK),
                    "supported_protocols": [
                        PROTOCOLS_MAPPING[k]
                        for k, v in atr.getSupportedProtocols().items()
                        if k in PROTOCOLS_MAPPING and v is True
                    ],
                },
            )
            asyncio.run_coroutine_threadsafe(self.websocket.send_json(response), self.loop)

        for card in removedcards:
            response = format_request(
                method="observer.card_removed",
                request_id=str(uuid.uuid4()),
                params={"reader": str(card.reader), "atr": toHexString(card.atr, PACK)},
            )
            asyncio.run_coroutine_threadsafe(self.websocket.send_json(response), self.loop)
