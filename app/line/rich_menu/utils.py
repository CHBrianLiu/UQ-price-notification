import logging
from typing import List

import requests

from app.config import app_config
from app.line.rich_menu.rich_menu_models import RichMenu


auth_header = {"Authorization": f"Bearer {app_config.LINE_LINE_BOT_CHANNEL_TOKEN}"}

# Get all rich menus
def get_rich_menus() -> List[RichMenu]:
    logging.info("Get rich menus")
    with requests.get(
        app_config.LINE_RICH_MENU_LIST_ENDPOINT, headers=auth_header
    ) as response:
        if not response.ok:
            raise RuntimeError(
                "Failed to get rich menu list with status code: %s and response: %s",
                response.status_code,
                response.content,
            )
        return [RichMenu.parse_obj(menu) for menu in response.json()["richmenus"]]


# Delete rich menu
def delete_rich_menu(menu_id: str):
    logging.info("Delete rich menu: %s", menu_id)
    with requests.delete(
        app_config.LINE_RICH_MENU_WITH_ID_ENDPOINT.format(id=menu_id),
        headers=auth_header,
    ) as response:
        if not response.ok:
            raise RuntimeError(
                "Failed to delete a rich menu with status code: %s and response: %s",
                response.status_code,
                response.content,
            )


# Create rich menu
def create_rich_menu(menu: RichMenu) -> RichMenu:
    logging.info("Create rich menu: %s", menu.name)
    with requests.post(
        app_config.LINE_RICH_MENU_ENDPOINT,
        headers=auth_header,
        json=menu.dict(exclude={"richMenuId"}, exclude_none=True),
    ) as response:
        if not response.ok:
            raise RuntimeError(
                "Failed to create a rich menu with status code: %s and response: %s",
                response.status_code,
                response.content,
            )
        menu.richMenuId = response.json()["richMenuId"]
        return menu


# Upload photo
def upload_rich_menu_background_image(menu_id: str, image_path: str):
    logging.info(
        "Upload rich menu image. image path: %s, menu_id: %s", image_path, menu_id
    )
    with open(image_path, "r") as image:
        with requests.post(
            app_config.LINE_RICH_MENU_IMAGE_ENDPOINT.format(id=menu_id),
            headers={**auth_header, "Content-Type": "image/png"},
            data=image.buffer,
        ) as response:
            if not response.ok:
                raise RuntimeError(
                    "Failed to upload a rich menu image with status code: %s and response: %s",
                    response.status_code,
                    response.content,
                )


# Make a rich menu default
def set_rich_menu_as_default(menu_id):
    logging.info("Set rich menu as default menu. %s", menu_id)
    with requests.post(
        app_config.LINE_RICH_MENU_DEFAULT_ENDPOINT.format(id=menu_id),
        headers=auth_header,
    ) as response:
        if not response.ok:
            raise RuntimeError(
                "Failed to set a rich menu as default with status code: %s and response: %s",
                response.status_code,
                response.content,
            )
