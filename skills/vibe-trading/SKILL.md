# Vibe-Trading: AI-Powered Multi-Agent Finance Workspace

Natural-language finance research AI agent with backtesting, strategy generation, and portfolio analysis across global markets (A-shares, HK/US equities, crypto).

## Trigger
Use this skill when the user wants to:
- Analyze stocks, crypto, or other financial instruments
- Run trading backtests
- Generate trading strategies from natural language
- Perform technical analysis (MACD, RSI, Ichimoku, Elliott Wave, etc.)
- Conduct quantitative research (factor analysis, pair trading, ML strategies)
- Analyze fundamentals (valuation, financial statements, earnings)
- Research macroeconomic trends and asset allocation
- Price options and analyze derivatives
- Deploy multi-agent swarm teams for collaborative financial analysis

## MCP Tools Available
This skill uses the `vibe-trading` MCP server which exposes 16 tools:
- `list_skills` / `load_skill` -- browse and load 64 finance skills
- `backtest` -- run historical backtests across markets
- `factor_analysis` -- IC/IR analysis and quantile backtesting
- `analyze_options` -- Black-Scholes pricing and Greeks
- `pattern_recognition` -- chart pattern detection
- `get_market_data` -- pull data from yfinance, tushare, OKX
- `read_url` / `read_document` / `read_file` / `write_file` -- data I/O
- `list_swarm_presets` / `run_swarm` / `get_swarm_status` -- multi-agent orchestration
- `get_run_result` / `list_runs` -- retrieve past analysis results

## Key Features
- 64 specialized finance skills across 8 domains
- 29 agent swarm team presets for collaborative analysis
- Cross-market backtest engines (A-share T+1, crypto funding/liquidation, US/HK fees)
- 15+ performance metrics and 4 portfolio optimizers
- Technical analysis, quant research, fundamental analysis, derivatives pricing

## CLI Usage (fallback)
If MCP tools are unavailable, use these commands directly:

```bash
# Interactive TUI
/Users/zhouql1978_1/Library/Python/3.12/bin/vibe-trading

# Single prompt
/Users/zhouql1978_1/Library/Python/3.12/bin/vibe-trading run -p "Backtest BTC-USDT MACD strategy"

# List skills
/Users/zhouql1978_1/Library/Python/3.12/bin/vibe-trading --skills

# List swarm presets
/Users/zhouql1978_1/Library/Python/3.12/bin/vibe-trading --swarm-presets
```

## Requirements
- OPENAI_API_KEY (or OpenRouter/DeepSeek compatible key) for agent features
- TUSHARE_TOKEN for A-share data (optional)
- yfinance (HK/US) and OKX (crypto) work without API keys
