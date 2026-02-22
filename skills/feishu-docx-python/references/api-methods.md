# API Methods Reference

## Document Operations

| Method | Description |
|--------|-------------|
| `client.docx.v1.document.create` | 创建文档 |
| `client.docx.v1.document.get` | 获取文档元信息 |
| `client.docx.v1.document.raw_content` | 获取文档原始内容(Markdown) |

## Block Operations

| Method | Description |
|--------|-------------|
| `client.docx.v1.document_block.get` | 获取单个块 |
| `client.docx.v1.document_block.list` | 获取文档所有块 |
| `client.docx.v1.document_block.patch` | 更新块内容 |
| `client.docx.v1.document_block.batch_update` | 批量更新块 |

## Block Children Operations

| Method | Description |
|--------|-------------|
| `client.docx.v1.document_block_children.get` | 获取子块列表 |
| `client.docx.v1.document_block_children.create` | 添加子块 |
| `client.docx.v1.document_block_children.batch_delete` | 删除子块 |

## Async Methods

All methods have async versions with `a` prefix:

- `client.docx.v1.document.acreate`
- `client.docx.v1.document_block.aget`
- `client.docx.v1.document_block_children.acreate`

## Request Options

| Parameter | Description |
|-----------|-------------|
| `document_id` | 文档ID |
| `block_id` | 块ID (根节点用文档ID) |
| `document_revision_id` | 文档版本 (-1 表示最新) |
| `client_token` | UUID，防止重复请求 |
| `user_id_type` | 用户ID类型 (`user_id` 或 `open_id`) |

## Error Handling

```python
response = client.docx.v1.document.create(request)

if not response.success():
    lark.logger.error(
        f"API failed: code={response.code}, msg={response.msg}, log_id={response.get_log_id()}")
    return

# Success - access data
lark.logger.info(lark.JSON.marshal(response.data, indent=4))
```

## Error Codes

See [error-codes.md](error-codes.md) for complete error codes (177xxxx) and solutions.
