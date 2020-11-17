=====
Usage
=====

To use pyscard JSON RPC in a project::

    import pyscard_json_rpc

API calls::

    {"jsonrpc": "2.0", "method": "smartcard.get_readers"}

    {"jsonrpc": "2.0", "method": "smartcard.connect", "params": {"reader": "Alcor Micro AU9560 00 00"}}

    {"jsonrpc": "2.0", "method": "connection.get_atr", "params": {"connection_id": "1a0d5cda-c0fa-4b6b-8585-14b4b27b3237"}}

    {"jsonrpc": "2.0", "method": "connection.transmit", "params": {"connection_id": "1a0d5cda-c0fa-4b6b-8585-14b4b27b3237", "apdu": "00a4020c020002"}}

    {"jsonrpc": "2.0", "method": "connection.disconnect", "params": {"connection_id": "1a0d5cda-c0fa-4b6b-8585-14b4b27b3237"}}
