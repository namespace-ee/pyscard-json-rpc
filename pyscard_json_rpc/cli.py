"""Console script for pyscard_json_rpc."""
import argparse
import sys
import uvicorn

from pyscard_json_rpc.app import app


def main():
    """Console script for pyscard_json_rpc."""
    parser = argparse.ArgumentParser()
    parser.add_argument("_", nargs="*")
    args = parser.parse_args()

    uvicorn.run(app, host="0.0.0.0", port=8020, log_level="debug")


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
