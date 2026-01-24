#!/usr/bin/env python3
"""
Random Price Data Graph Visualizer

Generates realistic stock-like random price data and displays it as an
interactive line chart in the browser using Chart.js.

Run this script and open http://localhost:8000 in a browser.
Refresh the page to generate new random price data.
"""

import random
import uuid
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from http.cookies import SimpleCookie
from urllib.parse import parse_qs


# Authentication configuration
PASSWORD = "password"
SESSION_TIMEOUT = 1800  # 30 minutes in seconds

# In-memory session storage: {session_token: expiry_timestamp}
active_sessions = {}


def generate_price_data(num_points=100, start_price=100.0, volatility=0.02, drift=0.0001):
    """
    Generate stock-like price data using a random walk algorithm.

    Args:
        num_points: Number of data points to generate
        start_price: Starting price value
        volatility: Standard deviation of returns (higher = more volatile)
        drift: Slight upward/downward bias

    Returns:
        List of price values
    """
    prices = [start_price]

    for _ in range(num_points - 1):
        # Random percentage change with drift
        change_percent = random.gauss(drift, volatility)
        new_price = prices[-1] * (1 + change_percent)
        # Ensure price doesn't go negative
        new_price = max(new_price, 0.01)
        prices.append(round(new_price, 2))

    return prices


def generate_html(prices):
    """
    Generate HTML with embedded Chart.js for displaying the price chart.

    Args:
        prices: List of price values

    Returns:
        HTML string
    """
    # Generate time labels (e.g., "Day 1", "Day 2", etc.)
    labels = [f"Day {i+1}" for i in range(len(prices))]

    # Determine color based on price movement
    start_price = prices[0]
    end_price = prices[-1]
    line_color = "#22c55e" if end_price >= start_price else "#ef4444"  # Green or red

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Stock Price Chart</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }}
        .container {{
            background: rgba(255, 255, 255, 0.05);
            border-radius: 16px;
            padding: 30px;
            width: 100%;
            max-width: 900px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            backdrop-filter: blur(10px);
        }}
        .header {{
            text-align: center;
            margin-bottom: 20px;
        }}
        h1 {{
            color: #ffffff;
            font-size: 24px;
            font-weight: 600;
            margin-bottom: 10px;
        }}
        .stats {{
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-bottom: 20px;
        }}
        .stat {{
            text-align: center;
        }}
        .stat-label {{
            color: #94a3b8;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .stat-value {{
            color: #ffffff;
            font-size: 20px;
            font-weight: 600;
        }}
        .stat-value.positive {{
            color: #22c55e;
        }}
        .stat-value.negative {{
            color: #ef4444;
        }}
        .chart-container {{
            position: relative;
            height: 400px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>ACME Corp Stock Price</h1>
        </div>
        <div class="stats">
            <div class="stat">
                <div class="stat-label">Start Price</div>
                <div class="stat-value">${start_price:.2f}</div>
            </div>
            <div class="stat">
                <div class="stat-label">Current Price</div>
                <div class="stat-value">${end_price:.2f}</div>
            </div>
            <div class="stat">
                <div class="stat-label">Change</div>
                <div class="stat-value {'positive' if end_price >= start_price else 'negative'}">
                    {'+' if end_price >= start_price else ''}{((end_price - start_price) / start_price * 100):.2f}%
                </div>
            </div>
        </div>
        <div class="chart-container">
            <canvas id="priceChart"></canvas>
        </div>
    </div>

    <script>
        const ctx = document.getElementById('priceChart').getContext('2d');

        const gradient = ctx.createLinearGradient(0, 0, 0, 400);
        gradient.addColorStop(0, '{line_color}33');
        gradient.addColorStop(1, '{line_color}00');

        new Chart(ctx, {{
            type: 'line',
            data: {{
                labels: {labels},
                datasets: [{{
                    label: 'Price ($)',
                    data: {prices},
                    borderColor: '{line_color}',
                    backgroundColor: gradient,
                    borderWidth: 2,
                    fill: true,
                    tension: 0.1,
                    pointRadius: 0,
                    pointHoverRadius: 6,
                    pointHoverBackgroundColor: '{line_color}',
                    pointHoverBorderColor: '#ffffff',
                    pointHoverBorderWidth: 2
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                interaction: {{
                    intersect: false,
                    mode: 'index'
                }},
                plugins: {{
                    legend: {{
                        display: false
                    }},
                    tooltip: {{
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        titleColor: '#ffffff',
                        bodyColor: '#ffffff',
                        padding: 12,
                        displayColors: false,
                        callbacks: {{
                            label: function(context) {{
                                return '$' + context.parsed.y.toFixed(2);
                            }}
                        }}
                    }}
                }},
                scales: {{
                    x: {{
                        grid: {{
                            color: 'rgba(255, 255, 255, 0.1)',
                            drawBorder: false
                        }},
                        ticks: {{
                            color: '#94a3b8',
                            maxTicksLimit: 10
                        }}
                    }},
                    y: {{
                        grid: {{
                            color: 'rgba(255, 255, 255, 0.1)',
                            drawBorder: false
                        }},
                        ticks: {{
                            color: '#94a3b8',
                            callback: function(value) {{
                                return '$' + value.toFixed(0);
                            }}
                        }}
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>
"""
    return html


def create_session():
    """
    Generate a new session token and store it with expiry timestamp.

    Returns:
        Session token string
    """
    session_token = str(uuid.uuid4())
    expiry_timestamp = time.time() + SESSION_TIMEOUT
    active_sessions[session_token] = expiry_timestamp
    return session_token


def is_session_valid(session_token):
    """
    Check if a session token is valid and not expired.
    Cleans up expired sessions.

    Args:
        session_token: Session token to check

    Returns:
        True if session is valid, False otherwise
    """
    if not session_token:
        return False

    # Cleanup expired sessions
    current_time = time.time()
    expired_tokens = [token for token, expiry in active_sessions.items() if expiry < current_time]
    for token in expired_tokens:
        del active_sessions[token]

    # Check if token exists and is not expired
    if session_token in active_sessions:
        return active_sessions[session_token] > current_time

    return False


def refresh_session(session_token):
    """
    Update the expiry timestamp for an active session.

    Args:
        session_token: Session token to refresh
    """
    if session_token in active_sessions:
        active_sessions[session_token] = time.time() + SESSION_TIMEOUT


def delete_session(session_token):
    """
    Remove a session from active sessions.

    Args:
        session_token: Session token to delete
    """
    if session_token in active_sessions:
        del active_sessions[session_token]


def generate_login_html(error_message=""):
    """
    Generate HTML for the login page.

    Args:
        error_message: Optional error message to display

    Returns:
        HTML string
    """
    error_html = ""
    if error_message:
        error_html = f'<div class="error">{error_message}</div>'

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - Stock Price Chart</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }}
        .container {{
            background: rgba(255, 255, 255, 0.05);
            border-radius: 16px;
            padding: 40px;
            width: 100%;
            max-width: 400px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            backdrop-filter: blur(10px);
        }}
        h1 {{
            color: #ffffff;
            font-size: 24px;
            font-weight: 600;
            margin-bottom: 30px;
            text-align: center;
        }}
        .form-group {{
            margin-bottom: 20px;
        }}
        label {{
            display: block;
            color: #94a3b8;
            font-size: 14px;
            margin-bottom: 8px;
        }}
        input[type="password"] {{
            width: 100%;
            padding: 12px 16px;
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 8px;
            color: #ffffff;
            font-size: 16px;
            transition: all 0.3s ease;
        }}
        input[type="password"]:focus {{
            outline: none;
            border-color: #22c55e;
            background: rgba(255, 255, 255, 0.15);
        }}
        button {{
            width: 100%;
            padding: 12px 16px;
            background: #22c55e;
            border: none;
            border-radius: 8px;
            color: #ffffff;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.3s ease;
        }}
        button:hover {{
            background: #16a34a;
        }}
        .error {{
            color: #ef4444;
            font-size: 14px;
            margin-bottom: 20px;
            text-align: center;
            padding: 10px;
            background: rgba(239, 68, 68, 0.1);
            border-radius: 8px;
            border: 1px solid rgba(239, 68, 68, 0.3);
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Stock Price Chart Login</h1>
        {error_html}
        <form method="POST" action="/login">
            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" required autofocus>
            </div>
            <button type="submit">Login</button>
        </form>
    </div>
</body>
</html>
"""
    return html


class PriceChartHandler(BaseHTTPRequestHandler):
    """HTTP request handler that serves the price chart."""

    def get_session_cookie(self):
        """
        Extract session token from Cookie header.

        Returns:
            Session token string or None if not found
        """
        cookie_header = self.headers.get('Cookie')
        if not cookie_header:
            return None

        cookie = SimpleCookie()
        cookie.load(cookie_header)

        if 'session_token' in cookie:
            return cookie['session_token'].value

        return None

    def set_session_cookie(self, session_token):
        """
        Generate Set-Cookie header for session token.

        Args:
            session_token: Session token to set in cookie
        """
        cookie = SimpleCookie()
        cookie['session_token'] = session_token
        cookie['session_token']['httponly'] = True
        cookie['session_token']['path'] = '/'
        self.send_header('Set-Cookie', cookie['session_token'].OutputString())

    def send_redirect(self, location):
        """
        Send 302 redirect response.

        Args:
            location: URL to redirect to
        """
        self.send_response(302)
        self.send_header('Location', location)
        self.end_headers()

    def do_GET(self):
        """Handle GET requests with authentication and routing."""
        # Handle logout
        if self.path == '/logout':
            session_token = self.get_session_cookie()
            if session_token:
                delete_session(session_token)
            self.send_redirect('/login')
            return

        # Handle login page
        if self.path == '/login':
            html = generate_login_html()
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html.encode())
            return

        # Handle main graph page (/ or /graph)
        if self.path == '/' or self.path == '/graph':
            session_token = self.get_session_cookie()

            # Check if session is valid
            if not is_session_valid(session_token):
                self.send_redirect('/login')
                return

            # Refresh session timeout
            refresh_session(session_token)

            # Generate fresh price data on each request
            prices = generate_price_data(
                num_points=100,
                start_price=100.0,
                volatility=0.025,
                drift=0.001
            )
            html = generate_html(prices)

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html.encode())
            return

        # Return 404 for other paths
        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'<html><body><h1>404 Not Found</h1></body></html>')

    def do_POST(self):
        """Handle POST requests for login."""
        # Handle login form submission
        if self.path == '/login':
            # Read request body
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')

            # Parse form data
            form_data = parse_qs(post_data)
            password = form_data.get('password', [''])[0]

            # Check password
            if password == PASSWORD:
                # Create new session
                session_token = create_session()

                # Send redirect with session cookie
                self.send_response(302)
                self.send_header('Location', '/')
                self.set_session_cookie(session_token)
                self.end_headers()
                return
            else:
                # Show login page with error
                html = generate_login_html(error_message="Invalid password")
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(html.encode())
                return

        # Return 404 for other POST paths
        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'<html><body><h1>404 Not Found</h1></body></html>')

    def log_message(self, format, *args):
        """Log HTTP requests."""
        print(f"{args[0]}")


def main():
    """Start the web server."""
    server_address = ('localhost', 8000)
    server = HTTPServer(server_address, PriceChartHandler)
    print("Server running at http://localhost:8000")
    print("Refresh the page to generate new random price data.")
    print("Press Ctrl+C to stop the server.")
    server.serve_forever()


if __name__ == "__main__":
    main()
