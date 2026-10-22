# JARVIS Voice Assistant

This project has two independent parts:

- `app.py`: the existing Flask website backend, including the Gemini-powered answer endpoint.
- `mcp_server.py`: a separate local MCP server with two safe demo tools. It does not call Gemini or read an API key.

The MCP server uses the official MCP Python SDK v2 and the standard `stdio` transport. Keep its output quiet in the terminal: MCP uses that channel to communicate with an MCP host.

## Requirements

- Python 3.11 or newer (Python 3.12 is fine)
- Internet access to install Python packages and, for the Inspector, Node.js with `npx`

## Install dependencies (Windows PowerShell)

Open PowerShell in this project folder and run:

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If PowerShell does not recognize `py -3.12`, use the installed Python 3.11+ launcher instead, such as `py -3.11`.

## Run the Flask app

In one PowerShell window, activate the environment if needed, then run:

```powershell
python app.py
```

Open `http://127.0.0.1:5000/` in a browser. The existing page/API behavior remains the same. To use Gemini, set `GEMINI_API_KEY` in the environment before starting Flask; never paste the key into `app.py`, `script.js`, or a public repository. Flask can still run its local commands without a Gemini key.

## Run and check the MCP server

The simplest protocol check uses the official MCP Inspector. In a second PowerShell window, from the project folder with the virtual environment active, run:

```powershell
mcp dev mcp_server.py
```

The Inspector opens in a browser. Select **Tools**, then run `get_current_datetime` and `jarvis_greeting`. You should see the current local date/time and a JARVIS online message. `mcp dev` needs Node.js and `npx` available on `PATH`.

To run the server directly for an MCP host that launches local stdio servers, use:

```powershell
python mcp_server.py
```

It will appear to wait silently. That is expected: an MCP host must connect to its standard input/output. Press `Ctrl+C` to stop it. Do not add `print()` statements to this server; use Python logging for diagnostics so the MCP protocol stream stays intact.

## Connect from an MCP host

Configure your MCP host to launch the absolute path to `mcp_server.py` with the same Python executable/environment where `mcp` is installed. For example, in an MCP host configuration the command can be the full path to `.venv\Scripts\python.exe`, with the full path to `mcp_server.py` as its argument. Restart the host after saving its configuration. Host configuration formats vary, so use that host's official MCP setup instructions.

The Flask app and MCP server are separate processes. Start whichever one you want to use; they can run at the same time in separate windows.

## Optional microphone assistant

`assistant.py` is the older standalone microphone version and is separate from both servers. It may need a working microphone and Windows speech engine. Install dependencies above, then run `python assistant.py`.

## Hackathon eligibility

Before signing up or submitting JARVIS to a hackathon, check the event's official eligibility rules with a parent or guardian. Do not bypass age requirements or account restrictions.

## Official MCP references

- [Official MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [SDK installation](https://py.sdk.modelcontextprotocol.io/get-started/installation/)
- [Running MCP servers and transports](https://py.sdk.modelcontextprotocol.io/run/)
