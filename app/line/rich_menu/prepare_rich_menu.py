import logging
from typing import List
from app.line.rich_menu.rich_menu_models import RichMenu
from app.config import app_config
from app.line.rich_menu import rich_menu, background_image_path
from app.line.rich_menu.utils import create_rich_menu, delete_rich_menu, set_rich_menu_as_default, upload_rich_menu_background_image, get_rich_menus


def setup():
    _delete_rich_menu_if_default_name_menu_exists(app_config.LINE_RICH_MENU_NAME, get_rich_menus())
    created_menu = create_rich_menu(rich_menu)
    upload_rich_menu_background_image(created_menu.richMenuId, background_image_path)
    set_rich_menu_as_default(created_menu.richMenuId)


def _delete_rich_menu_if_default_name_menu_exists(menu_name: str, menus: List[RichMenu]):
    for menu in menus:
        if menu.name == menu_name:
            logging.info("Old menu found. Delete it. ID: %s", menu.richMenuId)
            delete_rich_menu(menu.richMenuId)
