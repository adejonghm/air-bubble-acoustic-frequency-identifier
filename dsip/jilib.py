#!/usr/bin/env python3


"""
Dev: 	adejonghm
----------

JSON Interactive Library allows adding nodes and items on nodes,
removing items on nodes and renaming Keys, all in a JSON file.
"""


def add_node(json_file: list, node: dict, num_node: int = 1) -> list:
    """Add a new Node in the JSON file

    Args:
        json_file (list): JSON file after read.
        node (dict): New Node to be added.
        num_node (int, optional): Number of nodes to be added. By default it is 1.

    Returns:
        list: New JSON file ready to be serialized and saved.
    """
    data = json_file.copy()
    i = 0

    while i < num_node:
        data.append(node)
        i += 1

    return data


def add_item(json_file: list, key_name: str, key_value: str = "") -> list:
    """Add a new item {key: value} on all nodes in the JSON file.

    Args:
        json_file (list): JSON file after read.
        key_name (str): Name of the Key.
        key_value (optional): Value to be saved, it can be any type of data. By default it is empty.

    Returns:
        list: New JSON file ready to be serialized and saved.
    """

    data = json_file.copy()
    for node in data:
        node[key_name] = key_value

    return data


def del_item(json_file: list, key_name: str) -> list:
    """Remove an item from all nodes in the JSON file.

    Args:
        json_file (list): JSON file after read.
        key_name (str): Name of the Key.

    Returns:
        list: New JSON file ready to be serialized and saved.
    """
    data = json_file.copy()

    for node in data:
        node.pop(key_name)

    return data


def add_item_in_node(json_file: list, node: int, key_name: str, key_value: str = "") -> list:
    """Add a new item {key: value} on a specific node in the JSON file.

    Args:
        json_file (list): JSON file after read.
        node (int): Node number where the item will be added.
        key_name (str): Name of the Key.
        key_value (optional): Value to be saved, it can be any type of data. By default it is empty.

    Returns:
        list: New JSON file ready to be serialized and saved.
    """
    data = json_file.copy()
    data[node][key_name] = key_value

    return data


def del_item_in_node(json_file: list, node: int, key_name: str) -> list:
    """Remove a new item {key: value} on a specific node in the JSON file.

    Args:
        json_file (list): JSON file after read.
        node (int): Node number where the item will be added.
        key_name (str): Name of the Key.

    Returns:
        list: New JSON file ready to be serialized and saved.
    """
    data = json_file.copy()
    data[node].pop(key_name)

    return data


def rename_item(json_file: list, key_name: str, new_key_name: str) -> list:
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
