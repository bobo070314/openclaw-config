---
name: igp-mcp-bridge
description: "Connects to MCP servers using stdio transport. Supports tool listing, tool calling, and auto-reconnect with timeout."
license: MIT
compatibility:
 - igp-v4
metadata:
 author: IGP v4
 version: 1.0.0
 tags:
  - mcp
allowed-tools:
 - read
 - write
 - exec
---

# Igp Mcp Bridge Skill

## When to Activate
Activate this skill when the agent needs to interact with an external MCP (Model Context Protocol) server via standard input/output (stdio) — for example, to discover available tools, invoke remote capabilities like file operations or command execution, or maintain resilient communication during intermittent process restarts.

## Instructions
1. Configure the MCP server executable path and optional startup arguments in the agent’s runtime configuration under `igp-mcp-bridge` settings.
2. Initialize the bridge by invoking `mcp_connect()` — it starts the subprocess, establishes stdio-based MCP handshake, and retrieves the tool listing.
3. Use `mcp_list_tools()` to inspect available tools (e.g., `read`, `write`, `exec`) and their schemas before invocation.
4. Call remote tools via `mcp_call_tool(tool_name, arguments)` — the bridge serializes requests, handles stdio framing, and returns parsed responses.
5. The bridge automatically attempts reconnection up to 3 times with exponential backoff (1s → 2s → 4s) upon stdin/stdout disconnect, timing out after 10 seconds per attempt.

## Examples
A user asks: “Show me the contents of `config.json` in the current directory.”  
→ The agent activates `igp-mcp-bridge`, calls `mcp_call_tool("read", {"path": "config.json"})`, receives the file content via stdio, and returns it verbatim in its response.

## Notes
- The MCP server process must be executable and emit valid MCP JSON-RPC over stdio; invalid framing or malformed responses will cause call failures.
- Tool permissions (`read`, `write`, `exec`) are enforced both by this skill’s `allowed-tools` list and the underlying MCP server — unauthorized tool calls will be rejected.
- Auto-reconnect only triggers on stdio stream closure (e.g., server crash), not network errors — stdio transport implies local subprocess only.