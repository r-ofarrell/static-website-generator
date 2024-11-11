#!/usr/bin/env python3

from htmlnode import HTMLNode
from convert_blocks import markdown_to_block, block_to_block_type

def markdown_to_html_node(markdown):
    blocks = markdown_to_block(markdown)
    block_type_dict = {
        "heading": "h",
        "code": "code",
        "quote": "blockquote",
        "unordered_list": "ul",
        "ordered_list": "ol",
        "paragraph", "p"
    }
    for block in blocks:
        pass

# Order of operations
# 1. Split markdown into blocks using markdown_to_block
#   - So I will have markdown blocks like:
#       # Heading 1
#
#      Then some paragraph text that might have **bold**, *italic* and `code` in it.
#
#      * Unordered list1
#      * Unordered list2
#
#      ```Code block = x ```
#
# 2. Loop over each block.
#   - Determine the type of each block using block_to_block_type
#   - Based on the block type, create a new HTMLNode using the HTML class (init requires tag, value, children, and props)
#   - Then assign child HTMLNode objects (i.e., ParentNode and LeafNode) to HTMLNode
#     * Use text_to_textnode(text)
#
# 3.
