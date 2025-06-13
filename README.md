# Tornado Cash MCP

An MCP server that tracks Tornado Cash deposits and withdrawals to reveal hidden asset trails and wallet interactions.

![GitHub License](https://img.shields.io/github/license/kukapay/tornado-cash-mcp) 
![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![Status](https://img.shields.io/badge/status-active-brightgreen.svg)

## Features

- **Query Latest Deposits**: Retrieve the most recent deposit events with details including sender address (`from`), amount, block number, timestamp, and commitment.
- **Query Latest Withdrawals**: Fetch the latest withdrawal events with details including recipient address (`to`), amount, block number, and timestamp.

## Prerequisites

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) (recommended package manager)
- A valid [The Graph API key](https://thegraph.com/studio/) for accessing the Tornado Cash Subgraph

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/kukapay/tornado-cash-mcp.git
   cd tornado-cash-mcp
   ```

2. **install dependencies** using `uv`:
   ```bash
   uv sync
   ```

3. **Installing to Claude Desktop**:

    Install the server as a Claude Desktop application:
    ```bash
    uv run mcp install main.py --name "tornado-cash-mcp"
    ```

    Configuration file as a reference:

    ```json
    {
       "mcpServers": {
           "Tornado Cash": {
               "command": "uv",
               "args": [ "--directory", "/path/to/tornado-cash-mcp", "run", "main.py" ],
               "env": { "THEGRAPH_API_KEY": "the_graph_api_key"}               
           }
       }
    }
    ```
    Replace `/path/to/tornado-cash-mcp` with your actual installation path, and `the_graph_api_key` with your API key from The Graph.


## Tools

Use the MCP Inspector UI or integrate with a compatible client (e.g., Claude Desktop) to call the tools.

### Query Latest Deposits

Example prompt:
```
"Show me the latest 3 deposits from Tornado Cash."
```

Example output:
```
+------------+---------------+--------------+---------------------+--------------+
| from       | amount        | blockNumber  | time                | commitment   |
+============+===============+==============+=====================+==============+
| 0xdef...   |           0.1 | 12345678     | 2023-10-12 15:30:00 | 0xabc...     |
| 0xdee...   |             1 | 12345677     | 2023-10-12 15:28:20 | 0xabd...     |
| 0xdef...   |            10 | 12345676     | 2023-10-12 15:26:40 | 0xabe...     |
+------------+---------------+--------------+---------------------+--------------+
```

### Query Latest Withdrawals

Example prompt:
```
"Get the most recent 2 withdrawals from Tornado Cash."
```

Example output:
```
+------------+---------------+--------------+---------------------+
| to         | amount        | blockNumber  | time                |
+============+===============+==============+=====================+
| 0x789...   |             1 | 12345679     | 2023-10-13 14:40:00 |
| 0x78a...   |           100 | 12345678     | 2023-10-13 14:38:20 |
+------------+---------------+--------------+---------------------+
```

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

