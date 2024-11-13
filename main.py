#!/usr/bin/env python3

import os
import shutil
from pathlib import Path, PurePath


def remove_contents_of_public(directory):
    directory_path = Path(directory).absolute()
    for item in directory_path.iterdir():
        if item.is_file():
            item.unlink()
        else:
            remove_contents_of_public(item)
            print(f"Item to remove: {item}")
            item.rmdir()
    return
def copy_static_to_public(directory, destination):
    directory_path = Path(directory).absolute()
    destination_path = Path(destination).absolute()
    for item in directory_path.iterdir():
        if item.is_file():
            shutil.copy(item, destination_path)
        else:
            copy_static_to_public(item, destination_path)

    print(f"Final path: {directory_path}")
    return ""

    pass

if __name__ == "__main__":
    copy_static_to_public("static", "practice")
