---
name: feishu-docx-python
description: |
  Use when: (1) working with Feishu/Lark document API (docx), (2) creating or editing Feishu documents via Python SDK,
  (3) adding blocks (text, heading, list, quote, code, etc.) to Feishu documents, or when user mentions "飞书文档", "Feishu docx", or "lark docx".
---

# Feishu Document (docx) Python SDK

Use `lark_oapi` package to create and manipulate Feishu (飞书) cloud documents.

## Quick Start

```bash
pip install lark-oapi
```

## Core Workflow

### 1. Initialize Client

```python
import lark_oapi as lark
from lark_oapi.api.docx.v1 import *

client = lark.Client.builder() \
    .app_id("your_app_id") \
    .app_secret("your_app_secret") \
    .build()
```

### 2. Create Document

```python
request = CreateDocumentRequest.builder() \
    .request_body(CreateDocumentRequestBody.builder()
        .folder_token("fldxxxxxxxx")
        .title("文档标题")
        .build()) \
    .build()

response = client.docx.v1.document.create(request)
document_id = response.data.document.document_id
```

### 3. Add Blocks

**Critical**: Must set BOTH `block_type` AND content method.

```python
from lark_oapi.api.docx.v1.model import *

# Define constants (SDK doesn't include these)
class BlockType:
    TEXT = 2; HEADING1 = 3; HEADING2 = 4; HEADING3 = 5
    BULLET = 13; ORDERED = 14; CODE = 17; QUOTE = 18; DIVIDER = 19

# Helper: create text element
def text(content: str) -> TextElement:
    return TextElement.builder().text_run(
        TextRun.builder().content(content).build()
    ).build()

# Create block: heading + paragraph
blocks = [
    Block.builder()
        .block_type(BlockType.HEADING1)
        .heading1(Text.builder().elements([text("标题")]).build())
        .build(),
    Block.builder()
        .block_type(BlockType.TEXT)
        .text(Text.builder().elements([text("正文内容")]).build())
        .build(),
]

# Add to document root
request = CreateDocumentBlockChildrenRequest.builder() \
    .document_id(document_id) \
    .block_id(document_id) \
    .request_body(CreateDocumentBlockChildrenRequestBody.builder()
        .children(blocks).index(-1).build()) \
    .build()

client.docx.v1.document_block_children.create(request)
```

## Key Points

1. **block_type is required**: Always set BOTH `.block_type()` AND content method (`.heading1()`, `.text()`, etc.)
2. **Root block**: Use `document_id` as `block_id` to add to document root
3. **folder_token**: Required for creating documents - get from drive API
4. **Error handling**: Check `response.success()` before accessing data

## References

- **Block types**: See [block-types.md](references/block-types.md) for complete type constants and builder methods
- **API methods**: See [api-methods.md](references/api-methods.md) for all available methods
- **Error codes**: See [error-codes.md](references/error-codes.md) for complete error codes and solutions
- **Helper functions**: See [helpers.py](scripts/helpers.py) for reusable code
