# Stock Price Chart Visualizer

A standalone Python web application that generates and visualizes random stock-like price data using Chart.js. Features a clean, modern UI with password-protected access.

![Stock Price Chart](https://img.shields.io/badge/Python-3.x-blue.svg)
![No Dependencies](https://img.shields.io/badge/dependencies-none-green.svg)

## Features

- **Interactive Price Charts**: Real-time visualization of stock-like random walk data
- **Password Authentication**: Secure login screen with session management
- **Responsive Design**: Modern glass-morphism UI with dark gradient theme
- **Random Data Generation**: Each refresh generates new realistic price movements
- **Session Management**: 30-minute sessions with automatic timeout
- **Zero Dependencies**: Uses only Python standard library (Chart.js loaded from CDN)

## Quick Start

### Prerequisites

- Python 3.x (no external packages required)

### Installation

1. Clone or download this repository
2. Navigate to the project directory:

```bash
cd chromie
```

### Running the Application

Start the web server:

```bash
python3 price_graph.py
```

The server will start on `http://localhost:8000`

```
Server running at http://localhost:8000
Refresh the page to generate new random price data.
Press Ctrl+C to stop the server.
```

## Usage

1. **Access the application**: Open your browser and navigate to `http://localhost:8000`
2. **Login**: You'll be redirected to the login page
   - **Password**: `password`
3. **View the chart**: After successful login, you'll see the interactive stock price chart
4. **Generate new data**: Refresh the page to generate new random price data
5. **Logout**: Navigate to `http://localhost:8000/logout` to end your session

## Authentication

The application includes password-based authentication with the following features:

- **Hardcoded password**: `password` (configurable in `price_graph.py:18`)
- **Session duration**: 30 minutes of inactivity
- **Cookie-based sessions**: HttpOnly cookies for security
- **In-memory storage**: Sessions stored in memory (reset on server restart)

**Note**: This implementation is designed for localhost testing. For production use, implement proper password hashing and database-backed session storage.

## Technical Details

### Architecture

- **Single-file application**: All logic contained in `price_graph.py`
- **Built-in HTTP server**: Uses Python's `http.server` module
- **Random walk algorithm**: Generates realistic stock-like price movements using Gaussian distribution
- **Chart.js visualization**: Interactive line charts with hover tooltips

### Price Generation Parameters

Configure in `price_graph.py` lines 503-506:

```python
prices = generate_price_data(
    num_points=100,      # Number of data points
    start_price=100.0,   # Initial price
    volatility=0.025,    # Price movement volatility (higher = more volatile)
    drift=0.001          # Slight upward/downward bias
)
```

### Session Configuration

Configure in `price_graph.py` lines 18-19:

```python
PASSWORD = "password"              # Login password
SESSION_TIMEOUT = 1800            # Session timeout in seconds (30 minutes)
```

## Project Structure

```
chromie/
├── price_graph.py    # Main application file (all logic)
├── README.md         # This file
└── CLAUDE.md         # Development guidance for Claude Code
```

## API Endpoints

- `GET /` - Main stock chart (requires authentication)
- `GET /graph` - Alias for main chart (requires authentication)
- `GET /login` - Login page
- `POST /login` - Login form submission
- `GET /logout` - Logout and clear session

## Security Notes

This application is designed for **local development and testing only**:

- Password is stored in plain text
- Sessions are stored in memory (lost on restart)
- No HTTPS support
- No rate limiting on login attempts
- No CSRF protection

For production deployment, implement:
- Password hashing (bcrypt, argon2)
- Persistent session storage (Redis, database)
- HTTPS/TLS encryption
- Rate limiting and brute force protection
- CSRF tokens

## Customization

### Change Password

Edit line 18 in `price_graph.py`:

```python
PASSWORD = "your_new_password"
```

### Modify Chart Appearance

The visual style is defined in the `generate_html()` function (lines 261-458). Customize:
- Colors (line 277: `#22c55e` for positive, `#ef4444` for negative)
- Gradients (lines 78-79 for background)
- Chart dimensions (line 352)

### Adjust Price Volatility

Modify the `volatility` parameter for different price movement characteristics:
- `0.01`: Low volatility (stable prices)
- `0.025`: Medium volatility (default)
- `0.05`: High volatility (dramatic swings)

## Troubleshooting

**Port already in use**:
```bash
# Find process using port 8000
lsof -i :8000
# Kill the process
kill -9 <PID>
```

**Session expires immediately**:
- Check system time is correct
- Verify `SESSION_TIMEOUT` value in code

**Login doesn't work**:
- Ensure password matches exactly (case-sensitive)
- Check browser allows cookies
- Try clearing browser cookies for localhost

## License

This is a demonstration project. Use freely for learning and development purposes.

## Contributing

This is a standalone educational project. Feel free to fork and modify for your own use.
