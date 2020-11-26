=====
Usage
=====

To use pyscard JSON RPC in a project::

    import pyscard_json_rpc

Listening URL::

    ws://localhost:8040/ws/pyscard-json-rpc

API calls::

    {"jsonrpc": "2.0", "method": "smartcard.get_readers"}

    {"jsonrpc": "2.0", "method": "smartcard.connect", "params": {"reader": "Alcor Micro AU9560 00 00"}}

    {"jsonrpc": "2.0", "method": "connection.get_atr", "params": {"connection_id": "1a0d5cda-c0fa-4b6b-8585-14b4b27b3237"}}

    {"jsonrpc": "2.0", "method": "connection.transmit", "params": {"connection_id": "1a0d5cda-c0fa-4b6b-8585-14b4b27b3237", "apdu": "00a4020c020002"}}

    {"jsonrpc": "2.0", "method": "connection.disconnect", "params": {"connection_id": "1a0d5cda-c0fa-4b6b-8585-14b4b27b3237"}}


Observers requests::

    {"jsonrpc": "2.0", "method": "observer.reader_added", "id": "f55b0439-9fc6-4720-9023-8777b521ca89", "params": {"reader": "Generic Smart Card Reader Interface"}}

    {"jsonrpc": "2.0", "method": "observer.card_added", "id": "cb1266cc-9dd0-46f4-a729-deca5e10278c", "params": {"reader": "Generic Smart Card Reader Interface", "atr": "3BFE9600008031FE4380738400E065B0850400FB8290004E", "supported_protocols": [1, 2]}}

    {"jsonrpc": "2.0", "method": "observer.card_removed", "id": "25af5c07-e4d9-4e2c-a307-ceee7cebb63a", "params": {"reader": "Generic Smart Card Reader Interface", "atr": "3BFE9600008031FE4380738400E065B0850400FB8290004E"}}

    {"jsonrpc": "2.0", "method": "observer.reader_removed", "id": "0c3049cb-70f0-4ca8-9237-57390e3cc384", "params": {"reader": "Generic Smart Card Reader Interface"}}
