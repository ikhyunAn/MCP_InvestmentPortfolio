# Portfolio Manager MCP Server
<p align="center">
  <img src="assets/logo.png" width="300" alt="Project Logo">
</p>

<p align="center">
  <a href="https://mseep.ai/app/ikhyunan-mcp-investmentportfolio">
    <img src="https://mseep.net/pr/ikhyunan-mcp-investmentportfolio-badge.png" alt="MseeP.ai Security Assessment Badge" />
  </a>
</p>


A Model Context Protocol (MCP) server that provides tools and resources for managing and analyzing investment portfolios.

## Features

- **Portfolio Management**: Create and update investment portfolios with stocks and bonds
- **Market Data**: Fetch real-time stock price information and relevant news
- **Analysis**: Generate comprehensive portfolio reports and performance analysis
- **Recommendations**: Get personalized investment recommendations based on portfolio composition
- **Visualization**: Create visual representations of portfolio allocation

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/ikhyunAn/portfolio-manager-mcp.git
   cd portfolio-manager-mcp
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up API keys (optional):
   ```bash
   export ALPHA_VANTAGE_API_KEY="your_key_here"
   export NEWS_API_KEY="your_key_here"
   ```

   Alternatively, create a `.env` file in the root of the directory and store the API keys

## Usage

### Running the Server

You can run the server in two different modes:

1. **Stdio Transport** (default, for Claude Desktop integration):
   ```bash
   python main.py   # alternate commands: i.e.) python3, python3.11
   ```

2. **SSE Transport** (for HTTP-based clients):
   ```bash
   python main.py --sse
   ```

### Integration with Claude Desktop

Add the server to your Claude Desktop configuration file:

```json
{
  "mcpServers": {
    "portfolio-manager": {
      "command": "python",      // may use different command
      "args": ["/path/to/portfolio-manager-mcp/main.py"],
      "env": {
        "ALPHA_VANTAGE_API_KEY": "your_key_here",
        "NEWS_API_KEY": "your_key_here"
      }
    }
  }
}
```

If you choose to run your server in a virtual environment, then your configuration file will look like:

```json
{
  "mcpServers": {
    "portfolio-manager": {
      "command": "/path/to/portfolio-manager-mcp/venv/bin/python",
      "args": ["/path/to/portfolio-manager-mcp/main.py"],
      "env": {
        "PYTHONPATH": "/path/to/portfolio-manager-mcp",
        "ALPHA_VANTAGE_API_KEY": "your_key_here",
        "NEWS_API_KEY": "your_key_here"
      }
    }
  }
}
```

To run it in a virtual environment:

```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate  # On macOS/Linux
# or
# venv\Scripts\activate   # On Windows

# Install dependencies
pip install -r requirements.txt

# Run the server
python3 main.py
```


Or use the MCP CLI for easier installation:

```bash
mcp install main.py
```

## Example Queries

Once the server is running and connected to Claude, you can interact with it using natural language:

- "Create a portfolio with 30% AAPL, 20% MSFT, 15% AMZN, and 35% US Treasury bonds with user Id <User_ID>"
- "What's the recent performance of my portfolio?"
- "Show me news about the stocks in my portfolio"
- "Generate investment recommendations for my current portfolio"
- "Visualize my current asset allocation"

## Project Structure

```
portfolio-manager/
├── main.py                      # Entry point
├── portfolio_server/            # Main package
│   ├── api/                     # External API clients
│   │   ├── alpha_vantage.py     # Stock market data API
│   │   └── news_api.py          # News API
│   ├── data/                    # Data management
│   │   ├── portfolio.py         # Portfolio models
│   │   └── storage.py           # Data persistence
│   ├── resources/               # MCP resources
│   │   └── portfolio_resources.py # Portfolio resource definitions
│   ├── tools/                   # MCP tools
│   │   ├── analysis_tools.py    # Portfolio analysis
│   │   ├── portfolio_tools.py   # Portfolio management
│   │   ├── stock_tools.py       # Stock data and news
│   │   └── visualization_tools.py # Visualization tools
│   └── server.py                # MCP server setup
└── requirements.txt             # Dependencies
```

## Future Work

As of now, the MCP program uses manually created JSON file which keeps track of each user's investment portfolio.

This should be fixed so that it reads in the portfolio data from actual banking applications.


### Tasks

- [ ] Extract JSON from a Finance or Banking Application which the user uses
- [ ] Enable modifying the investment portfolio by the client
- [ ] Implement automated portfolio rebalancing
- [ ] Add support for cryptocurrency assets
- [ ] Develop mobile application integration

## License

MIT
