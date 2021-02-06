#!/usr/bin/env python3


"""
Dev: 	adejonghm
----------

JSON Interactive Library allows adding nodes and items on nodes,
removing items on nodes and renaming Keys, all in a JSON file.
"""


def add_node(json_file, node, num_node=1):
    """Add a new Node in the JSON file

    Args:
        json_file (list): JSON file after read.
        node (dict): New Node to be added.
        num_node (int, optional): Number of times to be added. Defaults to 1.

    Returns:
        list: New JSON file ready to be serialized and saved.
    """
    data = json_file.copy()

    for _ in range(num_node):
        data.append(node)

    return data


def add_item(json_file, key_name, key_value=""):
    """Add a new item {key: value} on all nodes in the JSON file.

    Args:
        json_file (list): JSON file after read.
        key_name (str): Name of the Key.
        key_value (optional): Value to be saved, it can be any type of data. Defaults to "".

    Returns:
        list: New JSON file ready to be serialized and saved.
    """

    data = json_file.copy()
    for i in data:
        i[key_name] = key_value

    return data


def add_item_in_node(json_file, node, key_name, key_value=""):
    """Add a new item {key: value} on a specific node in the JSON file.

    Args:
        json_file (list): JSON file after read.
        node (int): Node number where the item will be added.
        key_name (str): Name of the Key.
        key_value (optional): Value to be saved, it can be any type of data. Defaults to "".

    Returns:
        list: New JSON file ready to be serialized and saved.
    """

    data = json_file.copy()
    # node -= 1
    data[node][key_name] = key_value

    return data


def del_item(json_file, key_name):
    """Remove an item from all nodes in the JSON file.

    Args:
        json_file (list): JSON file after read.
        key_name (str): Name of the Key.

    Returns:
        list: New JSON file ready to be serialized and saved.
    """

    data = json_file.copy()
    for i in data:
        i.pop(key_name)

    return data


def rename_item(json_file, key_name, new_key_name):
    """Rename a specific Key on all nodes in the JSON file.

    Args:
        json_file (list): JSON file after read.
        key_name (str): Name of the Key.
        new_key_name (str): Name of the new.

    Returns:
        list: New JSON file ready to be serialized and saved.
    """

    data = json_file.copy()
    for i in data:
        value = i.pop(key_name)
        i[new_key_name] = value

    return data
