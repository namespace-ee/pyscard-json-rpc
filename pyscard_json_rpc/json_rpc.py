from typing import Optional, Dict

ERROR_CODES = {
    # our codes:
    423: "Locked",
    428: "Precondition Required",
    # JSON RPC Prefedined codes
    -32700: "Parse error",
    # Invalid JSON was received by the server. An error occurred on the server while parsing the JSON text.
    -32600: "Invalid Request",  # The JSON sent is not a valid Request object.
    -32601: "Method not found",  # The method does not exist / is not available.
    -32602: "Invalid params",  # Invalid method parameter(s).
    -32603: "Internal error",  # Internal JSON-RPC error.
    # -32000 to -32099:	"Server error"  # Reserved for implementation-defined server-errors.
}


def get_message_type(message: Dict) -> str:
    if message.get("jsonrpc") == "2.0":
        if "method" in message:
            return "request"
        elif "result" in message:
            return "success"
        elif "error" in message:
            return "error"
    raise ValueError("Message does not conform to JSON-RPC 2.0 standard")


def format_request(method: str, request_id: Optional[str], params: Optional[Dict] = None) -> Dict:
    data = {
        "jsonrpc": "2.0",
        "method": method,
    }
    if request_id is not None:
        data["id"] = request_id
    if params is not None:
        data["params"] = params
    return data


def format_error(
    code: int, message: Optional[str] = None, data: Optional[str] = None, request_id: Optional[str] = None
) -> Dict:
    error = {"code": code, "message": message or ERROR_CODES.get(code) or "Unknown error"}
    if data is not None:
        error["data"] = data
    data = {
        "jsonrpc": "2.0",
        "error": error,
    }
    if request_id is not None:
        data["id"] = request_id
    return data


def format_response(result, request_id: Optional[str]) -> Dict:
    data = {
        "jsonrpc": "2.0",
        "result": result,
    }
    if request_id is not None:
        data["id"] = request_id
    return data
