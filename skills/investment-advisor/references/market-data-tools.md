# 实时市场数据工具 — akshare + vibe-trading

> 本文件整合 akshare（A股/港股数据）和 vibe-trading（AI 交易研究）的实时市场能力，作为 investment-advisor 的"数据获取层"，与价值投资框架的"决策分析层"形成完整闭环。

---

## 一、设计理念

```
用户提问
    ↓
investment-advisor 决策分析层（段永平/Buffett/Dalio）
    ├── 需要历史智慧 → references/philosophy.md, company-analysis.md
    ├── 需要宏观判断 → references/dalio-principles.md
    └── 需要实时数据 → 本文件（akshare + vibe-trading）
    ↓
结构化建议（判断 + 数据 + 风险 + 语录 + 操作建议）
```

**核心原则**：数据是决策的输入，不是决策本身。所有数据获取必须服务于价值投资框架的分析需求，不做纯数据驱动的交易建议。

---

## 二、akshare — A股/港股数据获取

### 2.1 与价值投资框架对应的数据需求

| 分析维度 | 需要的数据 | akshare 接口 |
|----------|-----------|-------------|
| 存续判断 | 公司基本信息、上市年限 | `stock_individual_info_em` |
| 生意模式 | 毛利率、净利率、ROE、现金流 | `stock_financial_analysis_indicator` |
| 护城河 | 市占率、品牌溢价（价格 vs 行业） | `stock_sector_fund_flow_rank` |
| 估值研判 | PE、PB、PS、股息率 | `stock_a_indicator_lg`, `stock_zh_a_spot_em` |
| 基本面追踪 | 季度财报、营收/利润趋势 | `stock_financial_report_sina` |
| 行业对比 | 同行业估值水平 | `stock_board_industry_name_em` |
| 大盘估值 | 全市场 PE 中位数、破净率 | `stock_market_pe_lg` |
| 资金流向 | 主力资金、北向资金 | `stock_individual_fund_flow_rank`, `stock_hsgt_north_net_flow_in_em` |

### 2.2 核心代码模板

```python
import akshare as ak
import pandas as pd

# === 估值数据 ===
# 个股估值指标（PE/PB/PS/DV）
def get_valuation(symbol="600519"):
    """获取个股估值指标"""
    df = ak.stock_a_indicator_lg(symbol=symbol)
    return df.tail(1)[["trade_date", "pe", "pe_ttm", "pb", "ps", "dv_ratio"]]

# A股实时行情
def get_realtime(symbol="600519"):
    """获取实时行情"""
    df = ak.stock_zh_a_spot_em()
    row = df[df["代码"] == symbol]
    return row[["名称", "最新价", "涨跌幅", "市盈率-动态", "市净率", "总市值", "流通市值"]]

# === 财务数据 ===
# 利润表关键项
def get_income(symbol="600519"):
    """获取利润表"""
    return ak.stock_financial_report_sina(stock=symbol, symbol="利润表")

# 财务分析指标
def get_financial_indicator(symbol="600519"):
    """获取财务分析指标（ROE/毛利率/净利率等）"""
    return ak.stock_financial_analysis_indicator(symbol=symbol)

# === 行业与市场 ===
# 同行业估值对比
def get_industry_valuation():
    """获取行业板块估值"""
    return ak.stock_board_industry_name_em()

# 北向资金流向
def get_north_flow():
    """获取北向资金净流入"""
    return ak.stock_hsgt_north_net_flow_in_em(symbol="北上")

# 全市场PE
def get_market_pe():
    """获取全市场PE水平"""
    return ak.stock_market_pe_lg(symbol="000300")
```

### 2.3 使用场景与价值投资框架的对应

**场景 1：用户问"茅台现在贵不贵"**
1. akshare 取 PE_TTM、PB、股息率 → 与历史分位对比
2. 用段永平框架判断："安全边际=理解深度"，估值只是参考
3. 用 Dalio 框架判断：当前周期位置，法币贬值趋势下"不便宜"也可持有

**场景 2：用户问"帮我对比茅台和五粮液"**
1. akshare 取两家公司的 ROE、毛利率、净利率、PE、PB
2. 用段永平五维框架逐一对比
3. 结论：用数据说话，但最终决策基于"理解深度"

**场景 3：用户问"大盘现在什么位置"**
1. akshare 取全市场 PE 中位数、北向资金流向
2. 用 Dalio 周期框架定位
3. 给出仓位建议（繁荣期/泡沫期/危机期/重建期）

---

## 三、vibe-trading — AI 交易研究工具

### 3.1 功能概览

vibe-trading 是一个 AI 驱动的金融研究工具，提供：
- **自然语言查询**：用中文/英文描述研究需求，自动获取数据
- **技术分析**：K线形态、支撑/阻力位、技术指标
- **回测能力**：验证投资策略的历史表现
- **多数据源**：整合 akshare、yfinance、tushare 等多个数据源

### 3.2 使用方式

```bash
# CLI 直接查询
/Users/zhouql1978_1/Library/Python/3.12/bin/vibe-trading run -p "分析茅台近一年的K线走势和关键支撑位"

# 交互式对话
/Users/zhouql1978_1/Library/Python/3.12/bin/vibe-trading chat

# MCP 服务器模式（供 Claude Code 直接调用）
/Users/zhouql1978_1/Library/Python/3.12/bin/vibe-trading-mcp --transport stdio
```

### 3.3 与价值投资框架的关系

vibe-trading 的技术分析能力**不替代**价值投资决策，但在以下场景中提供补充信息：

| 场景 | vibe-trading 用途 | 决策由谁做 |
|------|-------------------|-----------|
| 确认买入时机 | 识别支撑位、超卖信号 | 段永平框架决定买不买，技术面辅助决定什么时候买 |
| 设置止损参考 | 识别关键支撑/阻力 | 仓位管理框架决定止损幅度 |
| 市场情绪判断 | 成交量变化、资金流向 | Dalio 框架判断周期位置 |
| 行业轮动参考 | 板块资金流向、强弱对比 | 不做轮动，但用于确认行业趋势 |
| 回测分红再投资 | 验证茅台 A/B 模型 | 用历史数据验证投资逻辑 |

### 3.4 铁则：技术分析在价值投资中的定位

1. **技术分析是辅助工具，不是决策工具**
2. **永远不因为技术指标而买入不懂的公司**
3. **技术分析只用于回答"什么时候"的问题，不回答"买不买"的问题**
4. **回测结果不等于未来表现**——段永平："过去不代表未来"
5. **短期的量价信号不改变长期持有决策**

---

## 四、数据 → 框架 → 建议的完整流程

### 标准分析流程

```
Step 1: 数据获取（akshare / vibe-trading）
  ├── 实时估值（PE/PB/股息率）
  ├── 财务指标（ROE/毛利率/净利率/现金流）
  ├── 行业对比
  └── 资金流向/市场情绪

Step 2: 框架分析
  ├── 段永平五维框架（存续/生意/护城河/风险/估值）
  ├── 巴菲特检查清单（懂不懂/10年/文化/替代/扛得住）
  ├── Dalio 周期定位（宏观环境/地缘风险/货币风险）
  └── 仓位管理规则（总仓位/单票上限/现金安全垫）

Step 3: 结构化输出
  ├── 核心判断（一句话）
  ├── 数据支撑（估值分位、财务趋势）
  ├── 分析依据（基于哪个框架/原则）
  ├── 关键风险（哪里可能出错）
  ├── 段永平/巴菲特怎么说（相关语录）
  └── 操作建议（仅当用户有持仓时）
```

### 快速数据获取模板（按问题类型）

| 用户问题类型 | 优先获取的数据 | 数据来源 |
|-------------|---------------|---------|
| "XX现在能不能买" | PE/PB历史分位 + 财务指标趋势 | akshare |
| "XX贵不贵" | PE_TTM、PB、PS、股息率 + 同行业对比 | akshare |
| "帮我分析XX" | 完整财务数据 + 行业对比 + 估值 | akshare |
| "大盘怎么样" | 全市场PE + 北向资金 + 行业资金流向 | akshare |
| "仓位怎么调" | 市场估值位置 + 持仓个股估值变化 | akshare |
| "XX的技术面怎么样" | K线走势 + 支撑阻力 + 成交量 | vibe-trading |
| "帮我回测XX策略" | 历史价格 + 分红数据 | vibe-trading |

---

## 五、数据获取代码片段（常用）

### 获取个股完整画像

```python
import akshare as ak

def stock_profile(symbol="600519"):
    """一键获取个股完整画像"""
    # 实时行情
    spot = ak.stock_zh_a_spot_em()
    row = spot[spot["代码"] == symbol].iloc[0]
    
    print(f"=== {row['名称']} ({symbol}) ===")
    print(f"最新价: {row['最新价']}")
    print(f"PE(动): {row['市盈率-动态']}")
    print(f"PB: {row['市净率']}")
    print(f"总市值: {row['总市值']}")
    
    # 估值指标
    val = ak.stock_a_indicator_lg(symbol=symbol).tail(1).iloc[0]
    print(f"PE_TTM: {val['pe_ttm']}")
    print(f"PS: {val['ps']}")
    print(f"股息率: {val['dv_ratio']}%")
    
    # 财务指标（最新季报）
    fin = ak.stock_financial_analysis_indicator(symbol=symbol).head(1).iloc[0]
    print(f"ROE: {fin.get('净资产收益率', 'N/A')}")
    print(f"毛利率: {fin.get('销售毛利率', 'N/A')}")
    print(f"净利率: {fin.get('销售净利率', 'N/A')}")
```

### 市场温度计

```python
def market_temperature():
    """市场温度计：大盘估值 + 资金流向"""
    # 沪深300 PE
    pe300 = ak.stock_market_pe_lg(symbol="000300").tail(1).iloc[0]
    print(f"沪深300 PE: {pe300['pe']}")
    
    # 北向资金
    north = ak.stock_hsgt_north_net_flow_in_em(symbol="北上").tail(5)
    print(f"近5日北向净流入:\n{north[['日期', '当日净流入']]}")
    
    # 行业资金流向TOP5
    sector = ak.stock_sector_fund_flow_rank(indicator="今日")
    print(f"资金流入TOP5行业:\n{sector.head(5)[['板块名称', '今日涨跌幅', '主力净流入-净额']]}")
```

---

## 六、注意事项

1. **akshare 数据有延迟**：实时行情延迟约 15 分钟，不适合高频交易（但价值投资者不需要高频数据）
2. **vibe-trading 需要 API Key**：部分功能需要 OpenAI 或其他 LLM API Key
3. **数据质量**：akshare 数据来源于东方财富、新浪等公开接口，可能存在偶发性错误，重要数据应交叉验证
4. **不替代独立思考**：所有数据都是为了辅助判断，最终决策必须基于价值投资框架的独立分析
