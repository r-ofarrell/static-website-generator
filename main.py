#!/usr/bin/env python3

import os
from pathlib import Path, PurePath

def copy_static_to_public(directory):
    directory_path = Path(directory).absolute()
    print(directory_path)
    for item in directory_path.iterdir():
        if item.is_file():
            print(item)
        else:
            print(f"Item: {item}")
            copy_static_to_public(item)

    print(f"Final path: {directory_path}")
    return ""

    pass

if __name__ == "__main__":
    copy_static_to_public("static")
