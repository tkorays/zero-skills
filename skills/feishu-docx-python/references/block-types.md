# Block Type Reference (1-27)

## Block Type Constants (官方文档)

The SDK does NOT include these constants. Define them in your code:

```python
class BlockType:
    # 1-11: 文本/标题块
    PAGE = 1           # 页面 Block - 文档根节点
    TEXT = 2           # 文本 Block - 普通段落
    HEADING1 = 3      # 标题 1 Block
    HEADING2 = 4      # 标题 2 Block
    HEADING3 = 5      # 标题 3 Block
    HEADING4 = 6      # 标题 4 Block
    HEADING5 = 7      # 标题 5 Block
    HEADING6 = 8      # 标题 6 Block
    HEADING7 = 9      # 标题 7 Block
    HEADING8 = 10     # 标题 8 Block
    HEADING9 = 11     # 标题 9 Block

    # 12-27: 其他块
    BULLET = 12       # 无序列表 Block
    ORDERED = 13       # 有序列表 Block
    CODE = 14         # 代码块 Block
    QUOTE = 15        # 引用 Block
    # 16: (保留)
    TODO = 17         # 待办事项 Block
    BITABLE = 18      # 多维表格 Block
    CALLOUT = 19      # 高亮块 Block
    CHAT_CARD = 20    # 会话卡片 Block
    DIAGRAM = 21      # 流程图 & UML Block
    DIVIDER = 22      # 分割线 Block
    FILE = 23         # 文件 Block
    GRID = 24         # 分栏 Block
    GRID_COLUMN = 25  # 分栏列 Block
    IFRAME = 26       # 内嵌网页 Block
    IMAGE = 27        # 图片 Block
```

## Block Builder Methods

| Type | Value | Builder Method | Data Type | Description |
|------|-------|----------------|-----------|-------------|
| PAGE | 1 | `.page(text)` | Text | 文档根节点 |
| TEXT | 2 | `.text(text)` | Text | 普通段落 |
| HEADING1 | 3 | `.heading1(text)` | Text | 标题 1 |
| HEADING2 | 4 | `.heading2(text)` | Text | 标题 2 |
| HEADING3 | 5 | `.heading3(text)` | Text | 标题 3 |
| HEADING4 | 6 | `.heading4(text)` | Text | 标题 4 |
| HEADING5 | 7 | `.heading5(text)` | Text | 标题 5 |
| HEADING6 | 8 | `.heading6(text)` | Text | 标题 6 |
| HEADING7 | 9 | `.heading7(text)` | Text | 标题 7 |
| HEADING8 | 10 | `.heading8(text)` | Text | 标题 8 |
| HEADING9 | 11 | `.heading9(text)` | Text | 标题 9 |
| BULLET | 12 | `.bullet(text)` | Text | 无序列表 |
| ORDERED | 13 | `.ordered(text)` | Text | 有序列表 |
| CODE | 14 | `.code(text)` | Text | 代码块 |
| QUOTE | 15 | `.quote(text)` | Text | 引用 |
| TODO | 17 | `.todo(text)` | Text | 待办事项 |
| BITABLE | 18 | `.bitable(bitable)` | Bitable | 多维表格 |
| CALLOUT | 19 | `.callout(callout)` | Callout | 高亮块 |
| CHAT_CARD | 20 | `.chat_card(chat_card)` | ChatCard | 会话卡片 |
| DIAGRAM | 21 | `.diagram(diagram)` | Diagram | 流程图/UML |
| DIVIDER | 22 | `.divider(divider)` | Divider | 分割线 |
| FILE | 23 | `.file(file)` | File | 文件 |
| GRID | 24 | `.grid(grid)` | Grid | 分栏 |
| GRID_COLUMN | 25 | `.grid_column(grid_column)` | GridColumn | 分栏列 |
| IFRAME | 26 | `.iframe(iframe)` | Iframe | 内嵌网页 |
| IMAGE | 27 | `.image(image)` | Image | 图片 |

## Text Element Styles

```python
# 加粗
TextElementStyle.builder().bold(True).build()

# 斜体
TextElementStyle.builder().italic(True).build()

# 删除线
TextElementStyle.builder().strikethrough(True).build()

# 下划线
TextElementStyle.builder().underline(True).build()

# 字体颜色
TextElementStyle.builder().fore_color("#FF0000").build()

# 背景色
TextElementStyle.builder().back_color("#FFFF00").build()

# 组合样式
TextElementStyle.builder() \
    .bold(True) \
    .italic(True) \
    .fore_color("#FF0000") \
    .build()
```

## Error Codes

| Error Code | Description | Solution |
|------------|-------------|----------|
| 99991400 | 触发频率限制 | 使用指数退避重试 |
| 99991401 | IP不在白名单 | 配置IP白名单 |
| 99991679 | 权限不足 | 检查token授权范围 |

## Notes

- **Type 16**: Reserved/unused
- **DIVIDER (22)**: 需要传入空对象 `{}`
- **Types 18, 23, 26, 27**: 需要额外数据(token/file_id等)
