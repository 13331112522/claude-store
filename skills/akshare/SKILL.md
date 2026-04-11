---
name: akshare
description: 使用 AKShare Python 库查看中国股票数据。用于涉及 A 股、港股、美股、股票行情、股票数据、股价、财务报表、资金流向、龙虎榜、融资融券等问题时。
---

# 中国股票数据 (China Stock Data)

This skill helps you query Chinese stock data using the AKShare Python library.

## How It Works

1. Identify the type of stock data the user wants (A-share, HK stock, US stock, etc.)
2. Use the appropriate AKShare function to fetch the data
3. Provide Python code examples and explain the output

## AKShare Installation

```bash
uv pip install akshare
```

或者使用 uv run 直接运行:

```bash
uv run --with akshare script.py
```

## 网络问题解决方案

如果在服务器环境（云服务器、VPS 等）访问东方财富等接口时遇到连接被拒绝或超时问题，可以使用 akshare-proxy-patch 插件。

### 安装

```bash
uv pip install akshare-proxy-patch
```

或使用 uv run:

```bash
uv run --with akshare,akshare-proxy-patch script.py
```

### 使用方法

在代码顶部添加以下两行：

```python
import akshare_proxy_patch
akshare_proxy_patch.install_patch("101.201.173.125", "", 30)

# 后续正常使用 akshare
import akshare as ak
df = ak.stock_individual_info_em(symbol="600703")
print(df)
```

### 命令行快速使用

```bash
uv run --with akshare,akshare-proxy-patch python -c "
import akshare_proxy_patch
akshare_proxy_patch.install_patch('101.201.173.125', '', 30)
import akshare as ak
df = ak.stock_individual_info_em(symbol='600703')
print(df)
"
```

### 参数说明

- 参数 1：网关地址（默认 `101.201.173.125`，不可修改）
- 参数 2：TOKEN（默认为空，每天可免费使用一定次数。如需更多，可注册申请）
- 参数 3：重试次数（默认 30）

### 支持的接口域名

- fund.eastmoney.com
- push2.eastmoney.com
- push2his.eastmoney.com

## Common Stock Data Queries

### A 股 (A-Shares) - Shanghai & Shenzhen

| Data Type | AKShare Function |
| --- | --- |
| 股票市场总貌 - 上交所 | `stock_sse_summary()` |
| 股票市场总貌 - 深交所 | `stock_szse_summary(date="YYYYMMDD")` |
| 个股信息 - 东财 | `stock_individual_info_em(symbol="000001")` |
| 个股信息 - 雪球 | `stock_individual_basic_info_xq(symbol="SH601127")` |
| 实时行情 | `stock_zh_a_spot_em()` |
| 历史行情 | `stock_zh_a_hist(symbol="000001", period="daily", start_date="20230101", end_date="20231231")` |
| 分时数据 | `stock_zh_a_minute(symbol="000001", period="5", adjust="qfq")` |
| 科创板行情 | `stock_zh_kc_spot_em()` |
| 科创板历史 | `stock_zh_kc_hist(symbol="688001", period="daily", start_date="20230101")` |

### 港股 (HK Stocks)

| Data Type | AKShare Function |
| --- | --- |
| 实时行情 - 东财 | `stock_zh_hk_spot_em()` |
| 实时行情 - 新浪 | `stock_zh_hk_spot_sina()` |
| 历史行情 | `stock_zh_hk_hist(symbol="00700", period="daily")` |
| 公司资料 | `stock_hk_info_em(symbol="00700")` |

### 美股 (US Stocks)

| Data Type | AKShare Function |
| --- | --- |
| 实时行情 - 东财 | `stock_zh_us_spot_em()` |
| 实时行情 - 新浪 | `stock_zh_us_spot_sina()` |
| 历史行情 | `stock_zh_us_hist(symbol="AAPL", period="daily")` |

### 财务报表 & 基本面

| Data Type | AKShare Function |
| --- | --- |
| 财务报表 - 东财 | `stock_financial_abstract_em(symbol="000001")` |
| 财务指标 | `stock_financial_analysis_indicator(symbol="000001")` |
| 十大股东 | `stock_zh_a_gdhs(symbol="000001")` |
| 十大流通股东 | `stock_zh_a_gdhs(symbol="000001", futype="1")` |
| 分红配送 | `stock_fh_em(symbol="000001")` |
| 业绩预告 | `stock_yjsy_em(symbol="000001")` |

### 资金流向 & 筹码

| Data Type | AKShare Function |
| --- | --- |
| 资金流向 - 同花顺 | `stock_moneyflow_hsgt(symbol="000001")` |
| 资金流向 - 东财 | `stock_moneyflow_em(symbol="000001", date="20240101")` |
| 筹码分布 | `stock_chip_distribution(symbol="000001")` |

### 龙虎榜 & 机构调研

| Data Type | AKShare Function |
| --- | --- |
| 龙虎榜 - 每日 | `stock_lhb_detail_em(date="20240101")` |
| 龙虎榜 - 上榜次数 | `stock_lhb_stat_em(start_date="20240101", end_date="20240131")` |
| 机构调研 - 统计 | `stock_jgdy_em(symbol="000001")` |
| 机构调研 - 详细 | `stock_jgdy_detail_em(symbol="000001")` |

### 融资融券 & 沪深港通

| Data Type | AKShare Function |
| --- | --- |
| 融资融券 | `stock_margin_em(symbol="000001")` |
| 沪深港通持股 | `stock_hk_hold_stats(symbol="000001")` |
| 沪深港通资金流向 | `stock_hsgt_global_em()` |

### 新股 & IPO

| Data Type | AKShare Function |
| --- | --- |
| 新股申购 | `stock_new_ipo()` |
| 新股上市首日 | `stock_new_share_first_em()` |
| 打新收益率 | `stock_ipo_pool()` |

### 板块 & 行业

| Data Type | AKShare Function |
| --- | --- |
| 概念板块 - 东财 | `stock_board_concept_name_em()` |
| 概念板块成分股 | `stock_board_concept_cons_em(symbol="人工智能")` |
| 行业板块 - 东财 | `stock_board_industry_name_em()` |
| 行业板块成分股 | `stock_board_industry_cons_em(symbol="新能源车")` |

### 估值 & 指标

| Data Type | AKShare Function |
| --- | --- |
| A 股估值指标 | `stock_valuation()` |
| 个股估值 | `stock_peddy(symbol="000001")` |
| 市盈率 - 主板 | `stock_market_pe()` |
| 市净率 | `stock_market_pb()` |

### 涨跌停 & 技术指标

| Data Type | AKShare Function |
| --- | --- |
| 涨停股池 | `stock_zt_pool_em(date="20240101")` |
| 跌停股池 | `stock_dt_pool_em(date="20240101")` |
| 创新高 | `stock_high_limit(symbol="000001")` |

### 停复牌 & 分红

| Data Type | AKShare Function |
| --- | --- |
| 停复牌信息 | `stock_tfp_em()` |
| 分红派息 | `stock_dividend_details()` |

### 大宗交易

| Data Type | AKShare Function |
| --- | --- |
| 大宗交易 - 市场统计 | `stock_block_trade_mm()` |
| 大宗交易 - 每日明细 | `stock_block_trade()` |

## Stock Code Format

- A 股: `"000001"` (深证) 或 `"600000"` (上证) 或 `"688001"` (科创板)
- 港股: `"00700"` 或 `"HK00700"`
- 美股: `"AAPL"` 或 `"NASDAQ:AAPL"`

## Usage Examples

### 查询 A 股实时行情

```bash
uv run --with akshare -c "
import akshare as ak
df = ak.stock_zh_a_spot_em()
print(df)
"
```

或者保存为脚本:

```python
import akshare as ak
df = ak.stock_zh_a_spot_em()
print(df)
```

```bash
uv run --with akshare script.py
```

### 查询个股历史 K 线

```python
import akshare as ak
df = ak.stock_zh_a_hist(symbol="000001", period="daily", start_date="20230101", end_date="20231231")
print(df)
```

```bash
uv run --with akshare script.py
```

### 查询股票基本信息

```python
import akshare as ak
df = ak.stock_individual_info_em(symbol="000001")
print(df)
```

```bash
uv run --with akshare script.py
```

### 查询财务报表

```python
import akshare as ak
df = ak.stock_financial_abstract_em(symbol="000001")
print(df)
```

```bash
uv run --with akshare script.py
```

### 查询资金流向

```python
import akshare as ak
df = ak.stock_moneyflow_em(symbol="000001", date="20240101")
print(df)
```

```bash
uv run --with akshare script.py
```

### 查询龙虎榜

```python
import akshare as ak
df = ak.stock_lhb_detail_em(date="20240101")
print(df)
```

```bash
uv run --with akshare script.py
```

## Important Notes

1. 实时行情数据在收盘后可能无法获取当日数据
2. 历史行情数据需要指定日期范围
3. 某些接口可能需要较长的 timeout 设置
4. 港股代码格式可能需要根据数据源调整

## Documentation

- AKShare 官网: https://akshare.akfamily.xyz/
- AKShare GitHub: https://github.com/akfamily/akshare
