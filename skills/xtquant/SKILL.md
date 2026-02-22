---
name: xtquant
description: |
  XtQuant Python量化交易库使用指南。使用场景：(1) 获取股票/期货/期权等行情数据, (2) 实现实盘交易(下单/撤单/查持仓), (3) 查询财务数据/板块信息, 
  (4) 编写量化策略脚本。当用户提到"xtquant"、"MiniQMT"、"量化交易"、"QMT实盘"时使用此skill。
---

# XtQuant 量化交易Python库

XtQuant是迅投MiniQMT的Python接口库，提供行情数据和交易功能。

## 核心概念

### 模块结构

| 模块 | 用途 | 导入方式 |
|------|------|----------|
| xtdata | 行情数据获取 | `from xtquant import xtdata` |
| xttrader | 实盘交易 | `from xtquant.xttrader import XtQuantTrader` |
| xtconstant | 交易常量 | `from xtquant import xtconstant` |
| xttype | 账户类型定义 | `from xtquant.xttype import StockAccount, FutureAccount` |

### 运行前置条件

1. **安装Python**: 64位 Python 3.6-3.13
2. **安装xtquant**: `pip install xtquant` 或将xtquant拷贝到Python的site-packages目录
3. **启动MiniQMT客户端**: 运行程序前必须先启动QMT/MiniQMT客户端并登录

### 代码格式

- 股票代码: `000001.SZ` (深圳) / `600000.SH` (上海)
- 期货代码: `IF2309.CFE` (股指期货) / `CU2309.SHFE` (沪铜)
- ETF代码: `510500.SH`

## 快速开始

### 1. 行情数据获取 (xtdata)

```python
from xtquant import xtdata

# 订阅实时行情
def on_data(datas):
    for stock_code in datas:
        print(stock_code, datas[stock_code])

xtdata.subscribe_quote('000001.SZ', period='1d', callback=on_data)
xtdata.run()  # 阻塞运行

# 获取历史K线
xtdata.download_history_data('000001.SZ', period='1d', start_time='20230101', end_time='20231231')
kline = xtdata.get_market_data(stock_list=['000001.SZ'], period='1d')
```

### 2. 实盘交易 (xttrader)

```python
from xtquant.xttrader import XtQuantTrader
from xtquant.xttype import StockAccount
from xtquant import xtconstant
import random

# 初始化交易接口
path = 'D:/QMT/userdata_mini'  # MiniQMT安装目录下的userdata_mini文件夹
session_id = random.randint(100000, 999999)
xt_trader = XtQuantTrader(path, session_id)
xt_trader.start()

# 连接账户
if xt_trader.connect() == 0:
    print("连接成功")

# 普通股票账户
account = StockAccount('123456789')

# 下单 (使用xtconstant常量)
order_id = xt_trader.order_stock(
    account,                          # 账户
    '600000.SH',                     # 股票代码
    xtconstant.STOCK_BUY,            # 委托类型: 买入
    100,                             # 委托数量
    xtconstant.FIX_PRICE,            # 报价类型: 指定价
    10.5,                            # 委托价格
    'strategy_name',                  # 策略名称
    'remark'                         # 备注
)
```

## 常用功能速查

### xtdata 行情模块

| 功能 | 函数 | 说明 |
|------|------|------|
| 订阅实时行情 | `subscribe_quote()` | 单股行情订阅 |
| 订阅全推行情 | `subscribe_whole_quote()` | 全市场行情 |
| 获取K线数据 | `get_market_data()` | 从缓存获取 |
| 获取本地数据 | `get_local_data()` | 从本地文件获取 |
| 下载历史数据 | `download_history_data()` | 补充历史数据 |
| 获取财务数据 | `get_financial_data()` | 三大报表等 |
| 获取板块列表 | `get_sector_list()` | 行业/概念板块 |
| 获取成分股 | `get_stock_list_in_sector()` | 板块成分股 |

### xttrader 交易模块 (正确API)

| 功能 | 函数 | 说明 |
|------|------|------|
| 股票下单 | `order_stock()` | 买入/卖出股票 |
| 股票异步下单 | `order_stock_async()` | 异步下单 |
| 撤单 | `cancel_order_stock()` | 撤销委托 |
| 订阅账户 | `subscribe()` | 订阅账户推送 |
| 反订阅 | `unsubscribe()` | 取消账户订阅 |
| 查资产 | `query_stock_asset()` | 查询账户资产 |
| 查持仓 | `query_stock_positions()` | 查询所有持仓 |
| 查持仓(单只) | `query_stock_position()` | 查询单只股票持仓 |
| 查委托 | `query_stock_orders()` | 查询所有委托 |
| 查委托(单笔) | `query_stock_order()` | 查询单笔委托 |
| 查成交 | `query_stock_trades()` | 查询所有成交 |

### 交易常量 (xtconstant)

**委托类型 (order_type):**
- `STOCK_BUY` - 股票买入
- `STOCK_SELL` - 股票卖出

**报价类型 (price_type):**
- `FIX_PRICE` - 指定价
- `LATEST_PRICE` - 最新价
- `MARKET_SH_CONVERT_5_CANCEL` - 最优五档即时成交剩余撤销(上海)

**委托状态 (order_status):**
- `ORDER_REPORTED` (50) - 已报
- `ORDER_SUCCEEDED` (56) - 已成
- `ORDER_CANCELED` (54) - 已撤
- `ORDER_JUNK` (57) - 废单

## 数据周期说明

```
tick        - 分笔数据
1m/5m/15m  - 分钟线
30m/1h     - 半小时/小时线
1d          - 日线
1w          - 周线
1mon        - 月线
1q          - 季度线
1hy         - 半年线
1y          - 年线
```

## 复权类型

```
none        - 不复权
front       - 前复权
back        - 后复权
front_ratio - 等比前复权
back_ratio  - 等比后复权
```

## 参考文档

详细API说明请参阅:
- **行情API**: [xtdata-api.md](references/xtdata-api.md)
- **交易API**: [xttrader-api.md](references/xttrader-api.md)
- **使用示例**: [examples.md](references/examples.md)

## 注意事项

1. 数据获取需先确保MiniQMT本地有所需数据，必要时用`download_history_data`补充
2. 实时行情订阅回调中不要执行耗时操作
3. 单股订阅建议不超过50只，大量订阅推荐使用全推数据
4. 板块等静态信息更新频率低，每周/每日定期下载即可
5. level2行情(逐笔/千档)仅实盘时有效，跨交易日自动清理
6. **重要**: 查询资产/持仓/委托前必须先调用 `subscribe(account)` 订阅账户
