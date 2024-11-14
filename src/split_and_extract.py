#!/usr/bin/env python3

import re
from src.textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes: list, delimiter: str, text_type: TextType) -> list:
    """Takes a list of nodes and returns the extracted bold, italic, and code markdown"""
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
    """Regex to find all instances of markdown images in a string"""
    image_markdown = re.findall(r"\B!\[([\w ]+)\]\((https:\/\/.*?\.[\w+ .\/=&%]+)\)", text)
    return image_markdown

def extract_markdown_links(text: str) -> tuple:
    """Regex to find all instances of markdown links in a string"""
    link_markdown = re.findall(r"(^| )(\[[\w ]+\]\([\w.:/$@&]+\))", text)
    return link_markdown

def split_nodes_image(old_nodes):
    """Takes a list of nodes and returns the extracted markdown images"""
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        original_text = node.text
        images_and_links = extract_markdown_images(node.text)
        if not images_and_links:
            new_nodes.append(node)
            continue

        for image in images_and_links:
            sections = original_text.split(f"![{image[0]}]({image[1]})")
            if len(sections) != 2:
                raise ValueError("Invalid markdown: image tag not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )

            original_text = sections[1]

        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    """Takes a list of nodes and returns the extracted markdown links"""
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        original_text = node.text
        images_and_links = extract_markdown_links(node.text)
        if not images_and_links:
            new_nodes.append(node)
            continue

        for link in images_and_links:
            name_and_url = re.search(r"\[([\w ]+)\]\(([\w .:/$%&@]+)\)", link[1])
            sections = original_text.split(f"[{name_and_url.group(1)}]({name_and_url.group(2)})")
            if len(sections) != 2:
                raise ValueError("Invalid markdown: link tag not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    name_and_url.group(1),
                    TextType.LINK,
                    name_and_url.group(2),
                )
            )

            original_text = sections[1]

        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def text_to_textnodes(text: str) -> list:
    """Takes a string of text and returns a list of TextNodes based on inline markdown"""
    node = [TextNode(text, TextType.TEXT)]
    delimiters = {"**": TextType.BOLD, "*": TextType.ITALIC, "`": TextType.CODE}
    for delimiter, text_type in delimiters.items():
        node = split_nodes_delimiter(node, delimiter, text_type)

    node = split_nodes_image(node)
    node = split_nodes_link(node)

    return node


if __name__ == "__main__":
    pass
