from app import config
import json
import logging
import os
from typing import Any, Dict, List, Union

logger = logging.getLogger()

PROJECT_ROOT_PATH = os.path.join(os.path.dirname(__file__), "../..")
CONFIG_FILE_PATH = os.path.join(PROJECT_ROOT_PATH, "config.json")
LOCAL_CONFIG_PATH = os.path.join(PROJECT_ROOT_PATH, "local.json")


def get_config_by_key(key: str) -> Union[Dict[str, Any], List[Any], str, int, float]:
    """Get config value by period-separated key, for instance, "logging.level".

    Args:
        key (str): period-separated key.

    Returns:
        Union[Dict[str, Any], List[Any], str, int, float]: config value
    """
    def get_config_by_keys(
        keys: List[str], config: Union[Dict[str, Any], Any]
    ) -> Union[Dict[str, Any], List[Any], str, int, float]:
        if not keys or not keys[0]:
            return config
        if not isinstance(config, dict):
            return config
        if keys[0] not in config:
            raise KeyError("No config found by provided key.")
        return get_config_by_keys(keys[1:], config[keys[0]])

    return get_config_by_keys(keys=key.split("."), config=get_config())


def get_config() -> dict:
    """Get whole config object, local file has higher priority

    Returns:
        dict: config object
    """
    def update_config_recursively(config: Dict[str, any], local_config: Dict[str, any]):
        for key in local_config.keys():
            if (
                key not in config
                or type(config[key]) is not type(local_config[key])
                or not isinstance(local_config[key], dict)
            ):
                config[key] = local_config[key]
            else:
                config[key] = update_config_recursively(config[key], local_config[key])
        return config

    config = _load_config(CONFIG_FILE_PATH)
    local_config = _load_config(LOCAL_CONFIG_PATH)
    return update_config_recursively(config, local_config)


def _load_config(file_path: str) -> dict:
    config = {}
    try:
        with open(file_path, "r") as config_file:
            config = json.load(config_file)
    except FileNotFoundError:
        logger.exception("Config file %r not found.", file_path)
        print("file not found")
    except json.JSONDecodeError:
        logger.exception("Invalid JSON content in config file.")
        print("error")

    return config
