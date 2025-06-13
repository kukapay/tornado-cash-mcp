import httpx
from mcp.server.fastmcp import FastMCP, Context
from tabulate import tabulate
from typing import Dict
from dotenv import load_dotenv
import os
import json
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Get The Graph API key from environment
THEGRAPH_API_KEY = os.getenv("THEGRAPH_API_KEY")
if not THEGRAPH_API_KEY:
    raise ValueError("THEGRAPH_API_KEY not found in .env file")

# Initialize MCP server
mcp = FastMCP("Tornado Cash MCP", dependencies=["httpx", "python-dotenv", "tabulate"])

# Subgraph GraphQL endpoint
SUBGRAPH_URL = "https://gateway.thegraph.com/api/subgraphs/id/DAaVDGqbwCJA1c3ccXqoYrBqWXAQ9nKaEnpFJSA2V7MP"

async def query_subgraph(query: str, variables: Dict = None) -> Dict:
    """Helper function to query the Tornado Cash Subgraph with API key."""
    headers = {
        "Authorization": f"Bearer {THEGRAPH_API_KEY}",
        "Content-Type": "application/json"
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(
            SUBGRAPH_URL,
            json={"query": query, "variables": variables or {}},
            headers=headers
        )
        response.raise_for_status()
        return response.json()

# Tool: Query Latest Deposits
@mcp.tool()
async def query_latest_deposits(limits: int = 10, ctx: Context = None) -> str:
    """
    Query the most recent deposits from Tornado Cash Subgraph and return results as a formatted table.

    Parameters:
        limits (int): The maximum number of deposit records to return. Must be positive. Default is 10.

    Returns:
        A string containing a tabulated representation of deposit records with columns: id, amount, timestamp, commitment, blockNumber, from.
    """
    if limits <= 0:
        raise ValueError("limits must be positive")
        
    query = """
    query LatestDeposits($first: Int, $orderBy: String, $orderDirection: String) {
      deposits(first: $first, orderBy: $orderBy, orderDirection: $orderDirection) {
        from
        amount
        blockNumber
        timestamp
        commitment
      }
    }
    """
    variables = {
        "first": limits,
        "orderBy": "timestamp",
        "orderDirection": "desc"
    }
    result = await query_subgraph(query, variables)
    deposits = result["data"]["deposits"]
    
    table_data = [
        [
            deposit["from"],
            deposit["amount"],
            deposit["blockNumber"],
            datetime.fromtimestamp(int(deposit["timestamp"])),
            deposit["commitment"][:10] + "...",
        ]
        for deposit in deposits
    ]    
    headers = ["from", "amount", "blockNumber", "timestamp", "commitment"]
    table = tabulate(table_data, headers=headers, tablefmt="grid")
    
    return table

# Tool: Query Latest Withdrawals
@mcp.tool()
async def query_latest_withdrawals(limits: int = 10, ctx: Context = None) -> str:
    """
    Query the most recent withdrawals from Tornado Cash Subgraph and return results as a formatted table.

    Parameters:
        limits (int): The maximum number of withdrawal records to return. Must be positive. Default is 10.

    Returns:
        A string containing a tabulated representation of withdrawal records with columns: id, amount, timestamp, to, blockNumber.
    """
    if limits <= 0:
        raise ValueError("limits must be positive")
        
    query = """
    query LatestWithdrawals($first: Int, $orderBy: String, $orderDirection: String) {
      withdrawals(first: $first, orderBy: $orderBy, orderDirection: $orderDirection) {
        to
        amount
        blockNumber
        timestamp
      }
    }
    """
    variables = {
        "first": limits,
        "orderBy": "timestamp",
        "orderDirection": "desc"
    }
    result = await query_subgraph(query, variables)
    withdrawals = result["data"]["withdrawals"]
    
    # Format withdrawals as a table
    table_data = [
        [
            withdrawal["to"],
            withdrawal["amount"],
            withdrawal["blockNumber"],
            datetime.fromtimestamp(int(withdrawal["timestamp"]))
        ]
        for withdrawal in withdrawals
    ]
    headers = ["to", "amount", "blockNumber", "time"]
    table = tabulate(table_data, headers=headers, tablefmt="grid")
    
    return table

if __name__ == "__main__":
    mcp.run()
