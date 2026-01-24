# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a standalone Python web application that generates and visualizes random stock-like price data using Chart.js. It consists of a single Python script (`price_graph.py`) that serves an interactive web-based price chart.

## Directory Structure

```
chromie/
├── price_graph.py    # Main application file
└── CLAUDE.md         # This file
```

## Running the Application

Navigate to the project directory and start the web server:
```bash
cd chromie
python3 price_graph.py
```

The server runs on `http://localhost:8000`. Each browser refresh generates new random price data.

## Architecture

**Single-file web server**: The application uses Python's built-in `http.server` module with a custom `PriceChartHandler` that:
1. Generates fresh random price data on each GET request using a random walk algorithm
2. Embeds the data into an HTML template with Chart.js
3. Serves the complete HTML page

**Key components**:
- `generate_price_data()`: Creates stock-like random walk data using Gaussian distribution with configurable volatility and drift
- `generate_html()`: Generates complete HTML with embedded Chart.js configuration and styling
- `PriceChartHandler`: HTTP handler that combines data generation and HTML serving

**No external dependencies**: Only uses Python standard library. Chart.js is loaded from CDN in the HTML.

## Modifying Price Generation

The price generation parameters are hardcoded in `PriceChartHandler.do_GET()` (lines 248-253):
- `num_points=100`: Number of data points
- `start_price=100.0`: Initial price
- `volatility=0.025`: Price movement volatility
- `drift=0.001`: Slight upward trend bias

Adjust these values to change the characteristics of generated price charts.
