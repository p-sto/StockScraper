"""Provides mechanism for dealing with configuration."""

import os
import json


def get_data_from_config(path_to_config: str) -> dict:
    """Return json representation of configuration file.

    :param path_to_config: path to configuration file
    :return: json object
    """
    if not os.path.exists(path_to_config):
        raise AttributeError('Provided path to config does not exist.')

    with open(path_to_config) as fil:
        return json.load(fil)
