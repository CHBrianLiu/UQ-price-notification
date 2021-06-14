import os

from app.line.messages import MessageAction, UriAction
from app.line.rich_menu.rich_menu_models import (
    RichMenu,
    RichMenuArea,
    RichMenuBounds,
    RichMenuSize,
)

project_root_path = os.path.join(os.path.dirname(__file__), "../../..")
background_image_path = os.path.join(project_root_path, "assets/rich menu.png")

help_add_action = RichMenuArea(
    bounds=RichMenuBounds(x=0, y=0, width=833, height=843),
    action=MessageAction(text="新增商品追蹤"),
)
list_action = RichMenuArea(
    bounds=RichMenuBounds(x=833, y=0, width=833, height=843),
    action=MessageAction(text="管理個人清單"),
)
go_website_action = RichMenuArea(
    bounds=RichMenuBounds(x=1666, y=0, width=833, height=843),
    action=UriAction(uri="https://www.uniqlo.com/tw/"),
)

rich_menu = RichMenu(
    size=RichMenuSize(width=2500, height=843),
    selected=True,
    name="Default",
    chatBarText="服務清單",
    areas=[help_add_action, list_action, go_website_action],
)
