#!/usr/bin/env python3

import re
from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes: list, delimiter: str, text_type: TextType) -> list:
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)

        else:
            split_nodes = []
            sections = ""
            if delimiter == "**":
                to_split = re.sub(r"(^\*\*|\*\*|\*\*$)", "#", node.text)
                sections = to_split.split("#")
            elif delimiter == "*":
                to_split = re.sub(r"(^\*|\*|\*$)", "#", node.text)
                sections = to_split.split("#")
            elif delimiter == "`":
                sections = re.split(r"^`|`{1}|`{1}|`$", node.text)
            if len(sections) % 2 == 0:
                raise Exception("Invalid Markdown syntax: No matching symbols")


            for i in range(len(sections)):
                if sections[i] == "":
                    continue
                if i % 2 == 0:
                    split_nodes.append(TextNode(sections[i], TextType.TEXT))
                else:
                    split_nodes.append(TextNode(sections[i], text_type))

            new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text: str) -> tuple:
    image_markdown = re.findall(r"!\[([\w ]+)\]\((https:\/\/.*?\.[a-z]+)\)", text)
    return image_markdown

def extract_markdown_link(text: str) -> tuple:
    link_markdown = re.findall(r"\[([\w ]+)\]\((https:\/\/.*?\.[a-z\/@]+)\)", text)
    return link_markdown

def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        split_nodes = []
        index = 0
        text = node.text
        extracted_images = extract_markdown_images(text)
        if not extracted_images:
            return ""
        sections = text.split("!")

        for i in sections:
            if i[0] == "[":
                split_nodes.append(TextNode(extracted_images[index][0], TextType.IMAGE, extracted_images[index][1]))
                index += 1
                words_after_image = re.search(r"( \w+ )", i)
                if words_after_image:
                    split_nodes.append(TextNode(words_after_image.group(1), TextType.TEXT))

            else:
                split_nodes.append(TextNode(i, TextType.TEXT))


        new_nodes.extend(split_nodes)
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        split_nodes = []
        index = 0
        text = node.text
        extracted_links = extract_markdown_link(text)
        if not extracted_links:
            return ""
        sections = text.split("[")

        for i in sections:
            if i.startswith("to"):
                split_nodes.append(TextNode(extracted_links[index][0], TextType.LINK, extracted_links[index][1]))
                index += 1
                words_after_image = re.search(r"( \w+ )", i)
                if words_after_image:
                    split_nodes.append(TextNode(words_after_image.group(1), TextType.TEXT))

            else:
                split_nodes.append(TextNode(i, TextType.TEXT))


        new_nodes.extend(split_nodes)
    return new_nodes
