# XtQuant 使用示例

本文件提供常见场景的完整代码示例。

---

## 1. 行情数据获取示例

### 1.1 获取单只股票历史K线

```python
from xtquant import xtdata

# 下载历史数据
xtdata.download_history_data('000001.SZ', period='1d', start_time='20230101', end_time='20231231')

# 获取数据
data = xtdata.get_market_data(
    stock_list=['000001.SZ'],
    period='1d',
    start_time='20230101',
    end_time='20231231'
)

# 提取收盘价
close_prices = data['close']
print(close_prices)
```

### 1.2 批量获取多只股票

```python
from xtquant import xtdata

stock_list = ['000001.SZ', '600000.SH', '600519.SH']

# 批量下载
xtdata.download_history_data2(
    stock_list=stock_list,
    period='1d',
    start_time='20230101',
    end_time='20231231',
    callback=lambda x: print(f"进度: {x}")
)

# 获取复权数据
data = xtdata.get_market_data(
    stock_list=stock_list,
    period='1d',
    dividend_type='front'  # 前复权
)
```

### 1.3 订阅实时行情

```python
from xtquant import xtdata

def on_quote(datas):
    """行情回调函数"""
    for stock_code in datas:
        data = datas[stock_code]
        if len(data) > 0:
            latest = data[-1]
            print(f"{stock_code}: {latest}")

# 订阅实时行情
xtdata.subscribe_quote(
    stock_code='000001.SZ',
    period='tick',  # 分笔数据
    callback=on_quote
)

# 阻塞运行
xtdata.run()
```

---

## 2. 板块与财务数据示例

### 2.1 获取板块成分股

```python
from xtquant import xtdata

# 先下载板块数据
xtdata.download_sector_data()

# 获取板块列表
sectors = xtdata.get_sector_list()
print(sectors[:10])  # 查看前10个板块

# 获取某板块成分股
stocks = xtdata.get_stock_list_in_sector('新能源汽车')
print(f"共{len(stocks)}只成分股")
```

### 2.2 获取财务数据

```python
from xtquant import xtdata

stock_list = ['000001.SZ', '600519.SH']

# 下载财务数据
xtdata.download_financial_data(
    stock_list=stock_list,
    table_list=['Balance', 'Income', 'CashFlow']
)

# 获取财务数据
financial_data = xtdata.get_financial_data(
    stock_list=stock_list,
    table_list=['Balance', 'Income']
)

# 提取净利润
for stock in stock_list:
    income_df = financial_data[stock]['Income']
    print(f"{stock} 净利润: {income_df['nIncome'].iloc[-1]}")
```

---

## 3. 实盘交易示例

### 3.1 完整交易流程

```python
from xtquant.xttrader import XtQuantTrader
from xtquant.xttype import StockAccount
from xtquant import xtconstant
import random
import time

# 配置
QMT_PATH = 'D:/QMT/userdata_mini'
ACCOUNT_ID = '8884926633'

# 1. 创建交易实例
session_id = random.randint(100000, 999999)
xt_trader = XtQuantTrader(QMT_PATH, session_id)

# 2. 启动交易通道
xt_trader.start()

# 3. 连接服务器
result = xt_trader.connect()
if result != 0:
    print(f"连接失败: {result}")
    exit()
print("连接成功")

# 4. 创建账户
account = StockAccount(ACCOUNT_ID)

# 5. 订阅账户 (重要！查询前必须订阅)
xt_trader.subscribe(account)

# 6. 查询资产
asset = xt_trader.query_stock_asset(account)
print(f"总资产: {asset.total_asset:.2f}")
print(f"可用资金: {asset.cash:.2f}")

# 7. 买入股票
order_id = xt_trader.order_stock(
    account=account,
    stock_code='600000.SH',
    order_type=xtconstant.STOCK_BUY,      # 委托类型: 买入
    volume=100,                          # 数量: 100股
    price_type=xtconstant.FIX_PRICE,    # 报价类型: 指定价
    price=10.50,                        # 价格: 10.50元
    strategy_name='my_strategy',
    remark=''
)
print(f"委托编号: {order_id}")

# 8. 等待成交
time.sleep(2)

# 9. 查询持仓
positions = xt_trader.query_stock_positions(account)
for pos in positions:
    print(f"{pos.stock_code}: {pos.volume}股, 成本{pos.avg_price:.2f}")

# 10. 卖出股票
order_id = xt_trader.order_stock(
    account=account,
    stock_code='600000.SH',
    order_type=xtconstant.STOCK_SELL,     # 委托类型: 卖出
    volume=100,
    price_type=xtconstant.FIX_PRICE,
    price=10.80
)

# 11. 撤单 (如有需要)
# xt_trader.cancel_order_stock(account, order_id)

# 12. 停止
xt_trader.stop()
```

### 3.2 期货交易

```python
from xtquant.xttrader import XtQuantTrader
from xtquant.xttype import FutureAccount
from xtquant import xtconstant

# 期货账户
fut_account = FutureAccount('账户ID', 'FUTURE')

# 开多仓
order_id = xt_trader.order_stock(
    fut_account,
    'IF2309.CFE',                      # 股指期货
    xtconstant.FUTURE_OPEN_LONG,        # 开多
    1,                                   # 1手
    xtconstant.FIX_PRICE,
    4000.0
)

# 平多仓
order_id = xt_trader.order_stock(
    fut_account,
    'IF2309.CFE',
    xtconstant.FUTURE_CLOSE_LONG_HISTORY, # 平昨多
    1,
    xtconstant.FIX_PRICE,
    4050.0
)
```

---

## 4. 异步下单示例

```python
from xtquant.xttrader import XtQuantTrader
from xtquant.xttype import StockAccount
from xtquant import xtconstant
import random

xt_trader = XtQuantTrader('D:/QMT/userdata_mini', random.randint(100000, 999999))
xt_trader.start()
xt_trader.connect()

account = StockAccount('8884926633')
xt_trader.subscribe(account)

# 异步下单 (返回请求序号seq)
seq = xt_trader.order_stock_async(
    account,
    '600000.SH',
    xtconstant.STOCK_BUY,
    100,
    xtconstant.FIX_PRICE,
    10.5,
    'my_strategy',
    ''
)
print(f"异步请求序号: {seq}")

# 需要在回调中处理结果
class MyCallback(XtQuantTraderCallback):
    def on_order_stock_async_response(self, response):
        print(f"异步下单回报: {response.order_id}, seq: {response.seq}")

xt_trader.register_callback(MyCallback())
xt_trader.run_forever()
```

---

## 5. 常见问题处理

### 5.1 数据未找到

```python
from xtquant import xtdata

stock_code = '000001.SZ'
period = '1d'

# 尝试获取
data = xtdata.get_market_data(stock_list=[stock_code], period=period)

if not data or data.get('close') is None:
    print("数据未找到，正在下载...")
    xtdata.download_history_data(stock_code, period, start_time='20200101')
    data = xtdata.get_market_data(stock_list=[stock_code], period=period)
```

### 5.2 连接失败重试

```python
from xtquant.xttrader import XtQuantTrader
import random

def connect_with_retry(path, max_retries=3):
    for i in range(max_retries):
        session_id = random.randint(100000, 999999)
        xt_trader = XtQuantTrader(path, session_id)
        xt_trader.start()
        
        result = xt_trader.connect()
        if result == 0:
            print(f"连接成功 (尝试 {i+1})")
            return xt_trader
        else:
            print(f"连接失败: {result}, 重试 {i+1}/{max_retries}")
            xt_trader.stop()
    
    raise Exception("连接失败")

xt_trader = connect_with_retry('D:/QMT/userdata_mini')
```

---

## 6. 注意事项

1. **先启动QMT客户端**: 任何xtquant操作前必须确保MiniQMT客户端已启动并登录
2. **路径格式**: Windows路径使用正斜杠 `D:/QMT/userdata_mini`
3. **必须订阅账户**: 调用 `subscribe(account)` 后才能查询资产/持仓/委托
4. **使用xtconstant常量**: 下单时使用 `xtconstant.STOCK_BUY` 等常量，不要用字符串
5. **回调线程安全**: 行情回调在独立线程执行，注意线程安全
6. **数据补充**: `get_market_data`前需确保本地有数据，必要时用`download_history_data`补充

---

## 7. 财务数据获取示例

### 7.1 获取股票财务数据(防超时版)

```python
from xtquant import xtdata

stock_code = '600879.SH'

# 1. 先下载财务数据(限制时间范围，避免超时)
xtdata.download_financial_data2(
    stock_list=[stock_code], 
    table_list=['Income', 'Balance', 'CashFlow'],
    start_time='20230101',  # 只下载2023年以来的数据
    end_time='20251231'
)

# 2. 获取数据
data = xtdata.get_financial_data(
    stock_list=[stock_code], 
    table_list=['Income', 'Balance', 'CashFlow'],
    start_time='20230101',
    end_time='20251231'
)

if stock_code in data:
    d = data[stock_code]
    
    # 利润表 - 注意字段名是下划线格式
    if 'Income' in d and len(d['Income']) > 0:
        inc = d['Income']
        print('===== 利润表 =====')
        
        # 去重处理
        seen = set()
        for i in range(len(inc)-1, -1, -1):
            row = inc.iloc[i]
            report_date = row.get('m_timetag', '')
            if report_date in seen:
                continue
            seen.add(report_date)
            
            # 兼容两种字段名格式
            revenue = row.get('operating_revenue', row.get('operatingRevenue', 0)) or 0
            profit = row.get('net_profit_incl_min_int_inc', row.get('netProfit', 0)) or 0
            
            print(f'{report_date}: 营收={revenue/1e8:.2f}亿, 净利润={profit/1e8:.2f}亿')
            
            if len(seen) >= 6:
                break
```

### 7.2 获取当前股价

```python
from xtquant import xtdata

stock_code = '600879.SH'

# 下载最近行情
xtdata.download_history_data(stock_code, period='1d', start_time='20250101')

# 获取收盘价
price_data = xtdata.get_market_data(
    stock_list=[stock_code], 
    period='1d', 
    count=1
)

if price_data and 'close' in price_data:
    current_price = price_data['close'].iloc[0, -1]
    print(f'当前股价: {current_price:.2f}元')
```

### 7.3 批量获取多只股票财务数据

```python
from xtquant import xtdata
import pandas as pd

stock_codes = ['600031.SH', '600879.SH', '000001.SZ']

# 批量下载(注意: 股票数量多时仍可能超时)
xtdata.download_financial_data2(
    stock_list=stock_codes, 
    table_list=['Income'],
    start_time='20230101',
    end_time='20251231'
)

# 获取数据
data = xtdata.get_financial_data(
    stock_list=stock_codes, 
    table_list=['Income'],
    start_time='20230101',
    end_time='20251231'
)

# 汇总净利润
for code in stock_codes:
    if code in data and 'Income' in data[code]:
        inc = data[code]['Income']
        if len(inc) > 0:
            latest = inc.iloc[0]
            profit = latest.get('net_profit_incl_min_int_inc', 0) or 0
            print(f'{code}: 净利润={profit/1e8:.2f}亿')
