#!/usr/bin/env python3

import os
import re
import shutil
from pathlib import Path, PurePath
from src.md_to_html_node import markdown_to_html_node


def remove_contents_of_public(directory):
    directory_path = Path(directory).absolute()
    for item in directory_path.iterdir():
        if item.is_file():
            item.unlink()
        else:
            remove_contents_of_public(item)
            item.rmdir()
    return


def copy_static_to_public(directory, destination):
    directory_path = Path(directory).absolute()
    destination_path = Path(destination).absolute()
    for item in directory_path.iterdir():
        if item.is_file():
            shutil.copy(item, destination_path)
        else:
            new_directory = destination_path.joinpath(item.name)
            new_directory.mkdir()
            copy_static_to_public(item, new_directory)

    return


def extract_title(markdown):
    heading = re.search(r"^#{1} ([\w ]+)", markdown)
    if not heading:
        raise Exception("Error: No h1 in markdown file")
    return heading.group(1).strip()

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, 'r', encoding='utf-8') as f:
        markdown = f.read()

    with open(template_path, 'r', encoding='utf-8') as t:
        template = t.read()

    template_copy = template
    html_nodes = markdown_to_html_node(markdown)
    html = html_nodes.to_html()
    heading = extract_title(markdown)
    template_copy = re.sub(r"{{ Title }}", heading, template_copy)
    template_copy = re.sub(r"{{ Content }}", html, template_copy)

    with open(dest_path, 'w', encoding='utf-8') as d:
        d.write(template_copy)



def main():
    remove_contents_of_public("public")
    copy_static_to_public("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")


if __name__ == "__main__":
    main()
