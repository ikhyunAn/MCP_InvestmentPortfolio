# MCP Server for Investment Portfolio Management

## Project Description

This MCP server is designed to help users track, analyze, and optimize their investment portfolios, consisting of stocks and bonds. 

### What is MCP?

MCP stands for Model Context Protocol.

| MCP is API interfaces exposed to AI. AI will by itself choose appropriate API interfaces, or methods, provided to them, and perform tasks on the user's local machine. 


To enable MCP, the user has to install both the client (Anthropic's Claude) and the server on the local machine. At its core, MCP follows a client-server architecture where a host application can connect to mulitiple servers to performs tasks.

For this particular project, an MCP Server will be implemented which will ***manage investment portfolio***.



### MCP Server Functionalities:

- Manage User Portfolios: Allow users to specify and update their portfolio items (stocks and bonds) along with their respective percentages.
- Fetch Portfolio Updates: Gather recent stock price changes (e.g., from yesterday or the past week) using external financial APIs.
- Aggregate Relevant News: Search the web for news related to the stocks in the user’s portfolio, using news APIs or web scraping.
- Generate Portfolio Reports: Create a report explaining recent changes in the portfolio’s value based on stock price movements and relevant news.
- Offer Investment Recommendations: Suggest adjustments to the portfolio based on the gathered data and analysis.
- The server will expose these capabilities through MCP resources and tools, enabling integration with LLM clients to deliver natural language reports and recommendations.

