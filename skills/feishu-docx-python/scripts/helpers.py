"""
Feishu Document SDK Helper Functions

Copy this file to your project and import as needed.
"""

from lark_oapi.api.docx.v1.model import *


# Block type constants (SDK doesn't include these)
class BlockType:
    # 1-11: 文本/标题块
    PAGE = 1  # 页面 Block
    TEXT = 2  # 文本 Block
    HEADING1 = 3  # 标题 1 Block
    HEADING2 = 4  # 标题 2 Block
    HEADING3 = 5  # 标题 3 Block
    HEADING4 = 6  # 标题 4 Block
    HEADING5 = 7  # 标题 5 Block
    HEADING6 = 8  # 标题 6 Block
    HEADING7 = 9  # 标题 7 Block
    HEADING8 = 10  # 标题 8 Block
    HEADING9 = 11  # 标题 9 Block

    # 12-27: 其他块
    BULLET = 12  # 无序列表 Block
    ORDERED = 13  # 有序列表 Block
    CODE = 14  # 代码块 Block
    QUOTE = 15  # 引用 Block
    # 16: (保留)
    TODO = 17  # 待办事项 Block
    BITABLE = 18  # 多维表格 Block
    CALLOUT = 19  # 高亮块 Block
    CHAT_CARD = 20  # 会话卡片 Block
    DIAGRAM = 21  # 流程图 & UML Block
    DIVIDER = 22  # 分割线 Block
    FILE = 23  # 文件 Block
    GRID = 24  # 分栏 Block
    GRID_COLUMN = 25  # 分栏列 Block
    IFRAME = 26  # 内嵌网页 Block
    IMAGE = 27  # 图片 Block


def text(content: str, bold: bool = False, italic: bool = False) -> TextElement:
    """Create a text element with optional styles."""
    style = None
    if bold or italic:
        style_builder = TextElementStyle.builder()
        if bold:
            style_builder = style_builder.bold(True)
        if italic:
            style_builder = style_builder.italic(True)
        style = style_builder.build()

    text_run = TextRun.builder().content(content)
    if style:
        text_run = text_run.text_element_style(style)

    return TextElement.builder().text_run(text_run.build()).build()


def heading_block(content: str, level: int = 1) -> Block:
    """Create a heading block (level 1-9)."""
    level = max(1, min(level, 9))  # Clamp to 1-9
    block_type = getattr(BlockType, f"HEADING{level}", BlockType.HEADING1)
    method_name = f"heading{level}"

    block = Block.builder().block_type(block_type)
    text_obj = Text.builder().elements([text(content)]).build()

    return getattr(block, method_name)(text_obj).build()


def paragraph(content: str) -> Block:
    """Create a paragraph block."""
    return (
        Block.builder()
        .block_type(BlockType.TEXT)
        .text(Text.builder().elements([text(content)]).build())
        .build()
    )


def bullet_item(content: str) -> Block:
    """Create a bullet list item."""
    return (
        Block.builder()
        .block_type(BlockType.BULLET)
        .bullet(Text.builder().elements([text(content)]).build())
        .build()
    )


def ordered_item(content: str) -> Block:
    """Create an ordered list item."""
    return (
        Block.builder()
        .block_type(BlockType.ORDERED)
        .ordered(Text.builder().elements([text(content)]).build())
        .build()
    )


def code_block(content: str) -> Block:
    """Create a code block."""
    return (
        Block.builder()
        .block_type(BlockType.CODE)
        .code(Text.builder().elements([text(content)]).build())
        .build()
    )


def quote(content: str) -> Block:
    """Create a quote block."""
    return (
        Block.builder()
        .block_type(BlockType.QUOTE)
        .quote(Text.builder().elements([text(content)]).build())
        .build()
    )


def divider() -> Block:
    """Create a divider block (type 22)."""
    return (
        Block.builder()
        .block_type(BlockType.DIVIDER)
        .divider(Divider.builder().build())
        .build()
    )


def todo(content: str, done: bool = False) -> Block:
    """Create a todo item block."""
    todo_text = Text.builder().elements([text(content)]).build()
    return Block.builder().block_type(BlockType.TODO).todo(todo_text).build()
