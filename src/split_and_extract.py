#!/usr/bin/env python3

import re
from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes: list, delimiter: str, text_type: TextType) -> list:
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        sections = node.text.split(delimiter)
        split_nodes = []
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown: Formatted section lacks closing tag")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            elif i % 2 == 1:
                split_nodes.append(TextNode(sections[i], text_type))
            else:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))

        new_nodes.extend(split_nodes)

    return new_nodes

def extract_markdown_images(text: str) -> tuple:
    image_markdown = re.findall(r"!\[([\w ]+)\]\((https:\/\/.*?\.[a-z]+)\)", text)
    return image_markdown

def extract_markdown_link(text: str) -> tuple:
    link_markdown = re.findall(r"[^!]\[([\w ]+)\]\((https:\/\/.*?\.[a-z\/@]+)\)", text)
    return link_markdown

def split_nodes_image(old_nodes):
    pass

def split_nodes_link(old_nodes):
    pass

def text_to_textnodes(text):
    pass

if __name__ == "__main__":
    pass
