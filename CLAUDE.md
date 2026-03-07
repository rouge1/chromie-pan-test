# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a standalone Python web application that generates and visualizes random stock-like price data using Chart.js. It consists of a single Python script (`price_graph.py`) that serves an interactive, password-protected web-based price chart.

## Directory Structure

```
chromie/
├── price_graph.py    # Main application file
├── README.md         # User-facing documentation
└── CLAUDE.md         # This file
```

## Running the Application

```bash
cd chromie
python3 price_graph.py
```

The server runs on `http://localhost:8000`. Visit `/login`, enter the password (`password`), then the chart is served at `/`. Each refresh generates new random price data.

## Architecture

**Single-file web server**: Uses Python's built-in `http.server` module with a custom `PriceChartHandler`.

**Key functions**:
- `generate_price_data()`: Random walk using Gaussian distribution with configurable volatility/drift
- `generate_html(prices)`: Full HTML page with embedded Chart.js chart
- `generate_login_html(error_message)`: Login page HTML
- `create_session()`: Creates UUID session token with expiry timestamp
- `is_session_valid(token)`: Validates token and cleans up expired sessions
- `refresh_session(token)`: Resets expiry on each authenticated request
- `delete_session(token)`: Removes session on logout

**PriceChartHandler routes**:
- `GET /` and `GET /graph` — serve chart (authentication required)
- `GET /login` — login page
- `POST /login` — validate password, set session cookie, redirect to `/`
- `GET /logout` — delete session, redirect to `/login`

**No external dependencies**: Only Python standard library. Chart.js loaded from CDN.

## Authentication

Configured at the top of `price_graph.py` (lines 21–22):
```python
PASSWORD = "password"
SESSION_TIMEOUT = 1800  # 30 minutes
```

Sessions are stored in the global `active_sessions` dict as `{token: expiry_timestamp}`. Sessions are lost on server restart. Cookies use `HttpOnly` flag.

**Security note**: Plain-text password, no rate limiting, no HTTPS, no CSRF protection. Suitable for local/LAN use only.

## Modifying Price Generation

Parameters in `PriceChartHandler.do_GET()` (lines 514–519):
```python
prices = generate_price_data(
    num_points=100,
    start_price=100.0,
    volatility=0.025,
    drift=0.001
)
```

## Deploying to LAN / Raspberry Pi

The server binds to `localhost` only (line 579). To allow connections from other devices on the network, change:
```python
server_address = ('', 8000)   # was ('localhost', 8000)
```

Then access via `http://<host-ip>:8000` from any device on the LAN.

## Common Pitfalls

- **Sessions reset on restart**: `active_sessions` is in-memory. Users must re-login after restarting the server.
- **Wrong line number references**: Line numbers shift as code grows. Prefer searching by function name rather than relying on hardcoded line references in documentation.
- **localhost binding blocks LAN access**: Default bind is `localhost`; must change to `''` or `0.0.0.0` for Raspberry Pi / multi-device access.
- **Chart.js requires internet**: The CDN script tag requires outbound internet access. For fully offline deployments, host Chart.js locally.
