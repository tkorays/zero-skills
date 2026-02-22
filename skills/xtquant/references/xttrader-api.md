# XtTrader API 参考手册

xttrader模块提供实盘交易功能，包括下单、撤单、查持仓等操作。

## 模块导入

```python
from xtquant.xttrader import XtQuantTrader, XtQuantTraderCallback
from xtquant.xttype import StockAccount
from xtquant import xtconstant
```

---

## 1. 初始化与连接

### XtQuantTrader - 创建交易实例

```python
xt_trader = XtQuantTrader(path, session_id)
```

**参数说明：**
| 参数 | 类型 | 说明 |
|------|------|------|
| path | str | MiniQMT安装目录下的userdata_mini文件夹路径 |
| session_id | int | 会话ID，建议使用随机数 |

**示例：**
```python
import random
path = 'D:/QMT/userdata_mini'
session_id = random.randint(100000, 999999)
xt_trader = XtQuantTrader(path, session_id)
```

---

### start - 启动交易通道

```python
xt_trader.start()
```

启动交易通道，必须在连接前调用。

---

### connect - 连接交易服务器

```python
xt_trader.connect()
```

**返回：** 0=成功，其他=失败

---

### subscribe - 订阅账户

```python
xt_trader.subscribe(account)
```

**重要**: 查询资产、持仓、委托前必须先订阅账户！

---

### stop - 停止交易

```python
xt_trader.stop()
```

---

## 2. 账户类型

### StockAccount - 普通股票账户

```python
from xtquant.xttype import StockAccount
account = StockAccount('账户ID')
# 或指定类型
account = StockAccount('账户ID', 'STOCK')
```

---

### FutureAccount - 期货账户

```python
from xtquant.xttype import FutureAccount
account = FutureAccount('账户ID', 'FUTURE')
```

---

## 3. 交易接口

### order_stock - 股票下单(同步)

```python
xt_trader.order_stock(account, stock_code, order_type, volume, price_type, price, strategy_name='', remark='')
```

**参数说明：**
| 参数 | 类型 | 说明 |
|------|------|------|
| account | StockAccount | 账户对象 |
| stock_code | str | 合约代码，如 `600000.SH` |
| order_type | int | 委托类型，使用xtconstant常量 |
| volume | int | 委托数量(股) |
| price_type | int | 报价类型，使用xtconstant常量 |
| price | float | 委托价格 |
| strategy_name | str | 策略名称 |
| remark | str | 备注 |

**委托类型 (order_type):**
- `xtconstant.STOCK_BUY` - 买入
- `xtconstant.STOCK_SELL` - 卖出

**报价类型 (price_type):**
- `xtconstant.FIX_PRICE` - 指定价
- `xtconstant.LATEST_PRICE` - 最新价
- `xtconstant.MARKET_SH_CONVERT_5_CANCEL` - 最优五档即时成交剩余撤销(上海)

**返回：** 委托编号 (int)

**示例：**
```python
# 买入100股
order_id = xt_trader.order_stock(
    account,
    '600000.SH',
    xtconstant.STOCK_BUY,      # 委托类型: 买入
    100,                       # 数量: 100股
    xtconstant.FIX_PRICE,      # 报价类型: 指定价
    10.5,                      # 价格: 10.5元
    'my_strategy',             # 策略名称
    ''                         # 备注
)
```

---

### order_stock_async - 股票异步下单

```python
xt_trader.order_stock_async(account, stock_code, order_type, volume, price_type, price, strategy_name='', remark='')
```

参数同 `order_stock`，返回异步请求序号(seq)。

---

### cancel_order_stock - 撤单

```python
xt_trader.cancel_order_stock(account, order_id)
```

**参数：** order_id - 委托编号

**返回：** True/False

---

## 4. 查询接口

### query_stock_asset - 查询账户资产

```python
xt_trader.query_stock_asset(account)
```

**返回：** XtAsset对象

**属性：**
```python
asset = xt_trader.query_stock_asset(account)
print(asset.account_id)    # 账户ID
print(asset.cash)         # 可用资金
print(asset.frozen_cash)  # 冻结资金
print(asset.market_value) # 持仓市值
print(asset.total_asset)  # 总资产
```

---

### query_stock_positions - 查询所有持仓

```python
xt_trader.query_stock_positions(account)
```

**返回：** List[XtPosition]

**Position属性：**
```python
positions = xt_trader.query_stock_positions(account)
for pos in positions:
    print(pos.stock_code)     # 合约代码
    print(pos.volume)        # 持仓数量
    print(pos.can_use_volume) # 可用数量
    print(pos.avg_price)     # 成本价
    print(pos.market_value)  # 市值
```

---

### query_stock_position - 查询单只股票持仓

```python
xt_trader.query_stock_position(account, stock_code)
```

---

### query_stock_orders - 查询所有委托

```python
xt_trader.query_stock_orders(account)
```

**返回：** List[XtOrder]

**Order属性：**
```python
orders = xt_trader.query_stock_orders(account)
for order in orders:
    print(order.order_id)     # 委托编号
    print(order.stock_code)  # 合约代码
    print(order.order_volume) # 委托数量
    print(order.price)       # 委托价格
    print(order.order_status) # 委托状态
```

---

### query_stock_order - 查询单笔委托

```python
xt_trader.query_stock_order(account, order_id)
```

---

### query_stock_trades - 查询所有成交

```python
xt_trader.query_stock_trades(account)
```

**返回：** List[XtTrade]

**Trade属性：**
```python
trades = xt_trader.query_stock_trades(account)
for trade in trades:
    print(trade.order_id)     # 委托编号
    print(trade.traded_id)   # 成交编号
    print(trade.stock_code)  # 合约代码
    print(trade.traded_volume) # 成交数量
    print(trade.traded_price)  # 成交价格
```

---

## 5. 回调接口

### register_callback - 注册回调

```python
class MyCallback(XtQuantTraderCallback):
    def on_disconnected(self):
        print("连接断开")
    
    def on_stock_order(self, order):
        print("委托回报:", order.order_id, order.order_status)
    
    def on_stock_trade(self, trade):
        print("成交回报:", trade.traded_id, trade.traded_volume)
    
    def on_order_error(self, order_error):
        print("下单失败:", order_error.order_id, order_error.error_msg)
    
    def on_cancel_error(self, cancel_error):
        print("撤单失败:", cancel_error.order_id, cancel_error.error_msg)

callback = MyCallback()
xt_trader.register_callback(callback)
```

---

## 6. 完整示例

```python
from xtquant.xttrader import XtQuantTrader, XtQuantTraderCallback
from xtquant.xttype import StockAccount
from xtquant import xtconstant
import random

# 配置
path = 'D:/QMT/userdata_mini'
account_id = '8884926633'

# 1. 创建交易实例
session_id = random.randint(100000, 999999)
xt_trader = XtQuantTrader(path, session_id)

# 2. 启动并连接
xt_trader.start()
result = xt_trader.connect()
print(f"连接结果: {result}")

# 3. 创建账户并订阅
account = StockAccount(account_id)
xt_trader.subscribe(account)

# 4. 查询资产
asset = xt_trader.query_stock_asset(account)
print(f"总资产: {asset.total_asset}")
print(f"可用资金: {asset.cash}")

# 5. 查询持仓
positions = xt_trader.query_stock_positions(account)
for pos in positions:
    print(f"{pos.stock_code}: {pos.volume}股")

# 6. 下单
order_id = xt_trader.order_stock(
    account, '600000.SH', 
    xtconstant.STOCK_BUY, 100, 
    xtconstant.FIX_PRICE, 10.5
)
print(f"委托编号: {order_id}")

# 7. 阻塞运行接收推送
xt_trader.run_forever()
```

---

## 委托状态说明

| 状态码 | 常量名 | 说明 |
|--------|--------|------|
| 48 | ORDER_UNREPORTED | 未报 |
| 49 | ORDER_WAIT_REPORTING | 待报 |
| 50 | ORDER_REPORTED | 已报 |
| 51 | ORDER_REPORTED_CANCEL | 已报待撤 |
| 52 | ORDER_PARTSUCC_CANCEL | 部成待撤 |
| 53 | ORDER_PART_CANCEL | 部撤 |
| 54 | ORDER_CANCELED | 已撤 |
| 55 | ORDER_PART_SUCC | 部成 |
| 56 | ORDER_SUCCEEDED | 已成 |
| 57 | ORDER_JUNK | 废单 |
| 255 | ORDER_UNKNOWN | 未知 |
