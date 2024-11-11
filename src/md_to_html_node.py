#!/usr/bin/env python3

import re
from htmlnode import HTMLNode, ParentNode, LeafNode
from split_and_extract import text_to_textnodes
from convert_blocks import (
    markdown_to_block,
    block_to_block_type,
    block_type_paragraph,
    block_type_heading,
    block_type_code,
    block_type_quote,
    block_type_unordered_list,
    block_type_ordered_list
    )

def markdown_to_html_node(markdown):
    blocks = markdown_to_block(markdown)
    block_type_dict = {
        "heading": "h",
        "code": "code",
        "quote": "blockquote",
        "unordered_list": "ul",
        "ordered_list": "ol",
        "paragraph": "p"
    }
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == block_type_heading:
            result = re.search(r"^(#{1,6})", block)
            block_type_dict["heading"] = f"h{len(result.group())}"
        # TODO convert blocks to html first
        print(f"Here is the block type: {block_type}")


"""
Order of operations
1. Split markdown into blocks using markdown_to_block
  - So I will have markdown blocks like:
      # Heading 1

     Then some paragraph text that might have **bold**, *italic* and `code` in it.

     * Unordered list1
     * Unordered list2

     ```Code block = x ```

2. Loop over each block.
  - Determine the type of each block using block_to_block_type
  - Based on the block type, create a new HTMLNode using the HTML class (init requires tag, value, children, and props)
  - Then assign child HTMLNode objects (i.e., ParentNode and LeafNode) to HTMLNode
    * Use text_to_textnode(text)

3.
"""

if __name__ == "__main__":
    block = """
# Here is the heading

Here is some paragraph.
With more paragraph.

> A quote looks **good** here

1. Point *one*
2. Point *two*
3. Point *three*

    """
    print(markdown_to_html_node(block))
