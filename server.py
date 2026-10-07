"""Run the MeshArc MCP server.

The server itself is `mesharc.mcp` in the `mesharc` package on PyPI
(source: https://github.com/mesharc-org/mesharc-python). This file starts it,
so the repository runs as it reads:

    pip install -r requirements.txt
    MESHARC_API_KEY=mesharc_... python server.py           # stdio
    python server.py --http --host 127.0.0.1 --port 8040    # hosted mode, see the README

Listing the tools needs no key; calling one needs MESHARC_API_KEY.
"""
from mesharc.mcp import main

if __name__ == "__main__":
    main()
