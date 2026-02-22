# XtData API 参考手册

xtdata模块提供行情数据获取功能，是xtquant的核心模块之一。

## 模块导入

```python
from xtquant import xtdata
```

---

## 1. 行情订阅接口

### subscribe_quote - 订阅单股行情

```python
xtdata.subscribe_quote(stock_code, period='1d', start_time='', end_time='', count=0, callback=None)
```

**参数说明：**
| 参数 | 类型 | 说明 |
|------|------|------|
| stock_code | str | 合约代码，如 `000001.SZ` |
| period | str | 数据周期，默认 `1d` |
| start_time | str | 起始时间，格式 `YYYYMMDD` 或 `YYYYMMDDHHmmss` |
| end_time | str | 结束时间 |
| count | int | 数据个数，0表示仅订阅实时数据 |
| callback | function | 数据回调函数 |

**回调函数格式：**
```python
def on_data(datas):
    # datas: {stock_code: [data1, data2, ...]}
    for stock_code in datas:
        print(stock_code, datas[stock_code])
```

**返回：** 订阅号 (大于0成功，-1失败)

---

### subscribe_whole_quote - 订阅全推行情

```python
xtdata.subscribe_whole_quote(code_list, callback=None)
```

**参数说明：**
| 参数 | 类型 | 说明 |
|------|------|------|
| code_list | list | 市场代码 `['SH', 'SZ']` 或合约代码列表 |

**返回：** 订阅号

---

### unsubscribe_quote - 反订阅

```python
xtdata.unsubscribe_quote(seq)
```

**参数：** seq - 订阅时返回的订阅号

---

### run - 阻塞运行

```python
xtdata.run()
```

阻塞当前线程，维持订阅回调运行。

---

## 2. 数据获取接口

### get_market_data - 获取行情数据

```python
xtdata.get_market_data(field_list=[], stock_list=[], period='1d', start_time='', end_time='', count=-1, dividend_type='none', fill_data=True)
```

**参数说明：**
| 参数 | 类型 | 说明 |
|------|------|------|
| field_list | list | 数据字段列表，空=全部字段 |
| stock_list | list | 合约代码列表 |
| period | str | 数据周期 |
| start_time | str | 起始时间 |
| end_time | str | 结束时间 |
| count | int | 数据个数，-1=全部 |
| dividend_type | str | 复权类型: `none/front/back/front_ratio/back_ratio` |
| fill_data | bool | 是否向后填充空缺数据 |

**返回：**
- K线数据: `dict {field: DataFrame}` - index为股票代码，columns为时间
- tick数据: `dict {stock_code: ndarray}`

---

### get_local_data - 获取本地数据

```python
xtdata.get_local_data(field_list=[], stock_list=[], period='1d', start_time='', end_time='', count=-1, dividend_type='none', fill_data=True, data_dir=None)
```

从本地数据文件快速获取历史数据，用法同 `get_market_data`。

---

### get_full_kline - 获取最新K线

```python
xtdata.get_full_kline(field_list=[], stock_list=[], period='1m', start_time='', end_time='', count=1, dividend_type='none', fill_data=True)
```

获取最新交易日K线全推数据（仅当日，不含历史）。

---

### get_full_tick - 获取全推数据

```python
xtdata.get_full_tick(code_list)
```

**参数：** `code_list` - 市场代码 `['SH', 'SZ']` 或合约列表

**返回：** `dict {stock: data}`

---

## 3. 数据下载接口

### download_history_data - 下载历史行情(单只)

```python
xtdata.download_history_data(stock_code, period, start_time='', end_time='', incrementally=None)
```

**参数说明：**
| 参数 | 类型 | 说明 |
|------|------|------|
| stock_code | str | 合约代码 |
| period | str | 数据周期 |
| start_time | str | 起始时间 |
| end_time | str | 结束时间 |
| incrementally | bool | 增量下载，None则根据start_time判断 |

---

### download_history_data2 - 批量下载历史行情

```python
xtdata.download_history_data2(stock_list, period, start_time='', end_time='', callback=None, incrementally=None)
```

**参数说明：**
| 参数 | 类型 | 说明 |
|------|------|------|
| stock_list | list | 合约代码列表 |
| period | str | 数据周期 |
| start_time | str | 起始时间 |
| end_time | str | 结束时间 |
| callback | function | 进度回调 `on_progress(data)` |

**进度回调格式：**
```python
def on_progress(data):
    # data: {'finished': 1, 'total': 50, 'stockcode': '000001.SZ', 'message': ''}
    print(data)
```

---

## 4. 财务数据接口

### get_financial_data - 获取财务数据

```python
xtdata.get_financial_data(stock_list, table_list=[], start_time='', end_time='', report_type='report_time')
```

**参数说明：**
| 参数 | 类型 | 说明 |
|------|------|------|
| stock_list | list | 合约代码列表 |
| table_list | list | 报表类型列表 |
| start_time | str | 起始时间 |
| end_time | str | 结束时间 |
| report_type | str | 报表筛选方式: `report_time`(截止日期) / `announce_time`(披露日期) |

**table_list 可选值：**
```python
['Balance']           # 资产负债表
['Income']            # 利润表
['CashFlow']          # 现金流量表
['Capital']           # 股本表
['Holdernum']         # 股东数
['Top10holder']       # 十大股东
['Top10flowholder']   # 十大流通股东
['Pershareindex']     # 每股指标
```

**返回：** `dict {stock: {table: DataFrame}}`

---

### download_financial_data / download_financial_data2 - 下载财务数据

```python
# 单只
xtdata.download_financial_data(stock_list, table_list=[])

# 批量带进度回调
xtdata.download_financial_data2(stock_list, table_list=[], start_time='', end_time='', callback=None)
```

---

## 5. 基础信息接口

### get_instrument_detail - 获取合约信息

```python
xtdata.get_instrument_detail(stock_code, iscomplete=False)
```

**返回字段 (基础)：**
- `ExchangeID` - 合约市场代码
- `InstrumentID` - 合约代码
- `InstrumentName` - 合约名称
- `OpenDate` - IPO日期(股票)
- `PreClose` - 前收盘价
- `UpStopPrice` - 涨停价
- `DownStopPrice` - 跌停价
- `FloatVolume` - 流通股本
- `TotalVolume` - 总股本

---

### get_instrument_type - 获取合约类型

```python
xtdata.get_instrument_type(stock_code)
```

**返回：** `dict {type: bool}`

**类型值：**
```python
'index'   # 指数
'stock'   # 股票
'fund'    # 基金
'etf'     # ETF
```

---

### get_trading_dates - 获取交易日列表

```python
xtdata.get_trading_dates(market, start_time='', end_time='', count=-1)
```

**参数：** `market` - 市场代码 `'SH'` / `'SZ'`

**返回：** `list` 时间戳列表

---

### get_sector_list - 获取板块列表

```python
xtdata.get_sector_list()
```

返回行业板块、概念板块列表

---

### get_stock_list_in_sector - 获取板块成分股

```python
xtdata.get_stock_list_in_sector(sector_name)
```

**参数：** `sector_name` - 板块名称，如 `'新能源汽车'`

**返回：** `list` 成分股代码列表

---

### download_sector_data - 下载板块分类

```python
xtdata.download_sector_data()
```

同步执行，下载板块分类信息

---

## 6. 其他接口

### get_divid_factors - 获取除权数据

```python
xtdata.get_divid_factors(stock_code, start_time='', end_time='')
```

### get_holidays - 获取节假日

```python
xtdata.get_holidays()
```

返回当年节假日列表

### get_trading_calendar - 获取交易日历

```python
xtdata.get_trading_calendar(market, start_time='', end_time='')
```

### get_ipo_info - 获取新股申购信息

```python
xtdata.get_ipo_info(start_time, end_time)
```

### get_period_list - 获取可用周期列表

```python
xtdata.get_period_list()
```

### get_cb_info - 获取可转债信息

```python
xtdata.get_cb_info(stockcode)
```

### get_etf_info - 获取ETF申赎信息

```python
xtdata.get_etf_info()
```

---

## 数据字段说明

### K线数据字段 (1m/5m/1d)

| 字段 | 说明 |
|------|------|
| time | 时间戳 |
| open | 开盘价 |
| high | 最高价 |
| low | 最低价 |
| close | 收盘价 |
| volume | 成交量 |
| amount | 成交额 |
| preclose | 前收价 |

### Tick数据字段

| 字段 | 说明 |
|------|------|
| time | 时间戳 |
| last | 最新价 |
| volume | 成交量 |
| amount | 成交额 |
| open_interest | 持仓量 |
| bid | 买价 |
| ask | 卖价 |

---

## ⚠️ 常见问题与注意事项

### 1. 下载超时问题

**问题**: 批量下载财务数据时容易超时

**解决方案**:
- 使用 `start_time` 和 `end_time` 限制下载范围
- 建议每次只下载最近2-3年的数据
- 使用 `download_financial_data2` 带进度回调

```python
# 推荐：限制时间范围，避免超时
xtdata.download_financial_data2(
    stock_list=['600879.SH'], 
    table_list=['Income'],
    start_time='20230101',  # 只下载2023年以来的数据
    end_time='20251231'
)
```

### 2. 财务数据字段名问题

**问题**: 获取的财务数据字段名为空或0

**原因**: 字段名可能是下划线格式而非驼峰格式

**解决方案**: 先打印列名确认实际字段

```python
data = xtdata.get_financial_data(stock_list=['600879.SH'], table_list=['Income'])
inc = data['600879.SH']['Income']
print('可用字段:', list(inc.columns))  # 先检查实际字段名

# 常用字段名映射（兼容两种格式）
revenue = row.get('operating_revenue', row.get('operatingRevenue', 0))
profit = row.get('net_profit_incl_min_int_inc', row.get('netProfit', 0))
```

### 3. 参数名注意事项

| 接口 | 注意事项 |
|------|----------|
| `download_financial_data` | 参数是 `stock_list` 不是 `stock_code` |
| `download_history_data` | 不支持 `count` 参数，用 `start_time`/`end_time` 控制 |
| `get_market_data` | `count`: -1=全部, >0=限制个数 |

### 4. 财务数据去重

**问题**: 返回的数据可能有重复行

**解决方案**:
```python
seen = set()
for i in range(len(inc)-1, -1, -1):
    report_date = inc.iloc[i].get('m_timetag', '')
    if report_date in seen:
        continue
    seen.add(report_date)
    # 处理数据
```

### 5. 每股指标为空

**问题**: `Pershareindex` 表数据可能为空或0

**建议**: 使用 `Income` 表计算或从其他数据源获取
