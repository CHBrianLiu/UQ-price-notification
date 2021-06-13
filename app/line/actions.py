import logging
from typing import Any, Dict, List

from app.config import app_config
from app.line.messages import (
    ButtonTemplateMessage,
    CarouselTemplateColumn,
    CarouselTemplateImageRatio,
    CarouselTemplateMessage,
    ConfirmTemplateMessage,
    MessageAction,
    TemplateMessage,
    UriAction,
)
from app.line.reply_messages import ResponseMessageType
from app.line.utils import compose_product_carousel
from app.models.data_store import data_access
from app.models.Product import Product
from app.models.standard_model import DatabaseOperationError
from app.models.User import User
from app.uq.product import NoUqProduct, UqProduct


async def add_tracking_product(user_id: str, product_id: str) -> ResponseMessageType:
    try:
        product = await UqProduct.create(product_id)
    except NoUqProduct:
        logging.warning("Product ID invalid: %s", product_id)
        return ("not_found", {})

    # Mew user, copy from template
    user_data = (
        data_access.get_user_info(user_id)
        if data_access.has_user(user_id)
        else User(user_id=user_id, count_tracking=0, product_tracking=[])
    )

    # Product has been tracked
    if product_id in user_data.product_tracking:
        return ("in_list", {"title": product.product_name})

    if user_data.count_tracking >= app_config.TRACKING_ITEM_MAXIMUM:
        return ("reach_limit", _create_confirm_template_for_reaching_limit())

    user_data.product_tracking.add(product_id)
    user_data.count_tracking += 1

    # Create product
    if not data_access.is_product_tracked_by_any_user(product_id):
        data_access.update_product(Product(product_id=product_id))

    # update user record
    data_access.update_user(user_data)

    return ("tracking", {"title": product.product_name})


def _create_confirm_template_for_reaching_limit():
    manage_list_action = MessageAction(text="list", label="我的追蹤清單")
    cancel_action = MessageAction(text="cancel", label="我知道了！")
    confirm_template = ConfirmTemplateMessage(
        text="你的追蹤清單已滿！\n來整理一下你的清單吧！", actions=[manage_list_action, cancel_action]
    )
    return TemplateMessage(
        altText="You've reached the limit of number of tracking items.",
        template=confirm_template,
    ).dict(exclude_none=True)


async def confirm_product_adding(product_id: str) -> ResponseMessageType:
    try:
        product = await UqProduct.create(product_id)
    except NoUqProduct:
        logging.warning("Product ID invalid: %s", product_id)
        return ("not_found", {})

    button_template = _create_button_template(product)
    alt_text = f"To add {product.product_name} to your tracking list, type:\nadd {product.product_id}"

    return (
        "confirm",
        TemplateMessage(altText=alt_text, template=button_template).dict(
            exclude_none=True
        ),
    )


def _create_button_template(product: UqProduct) -> Dict[str, Any]:
    add_action_button = MessageAction(text=f"add {product.product_id}", label="Yes")
    cancel_action_button = MessageAction(text="cancel", label="No")
    return ButtonTemplateMessage(
        title=product.product_name,
        text=f"{app_config.UQ_PRODUCT_CURRENCY}{product.product_derivatives_lowest_price}\n你要追蹤此商品嗎？",
        thumbnailImageUrl=product.product_image_url,
        actions=[add_action_button, cancel_action_button],
    )


def delete_tracking_product(user_id: str, product_id: str) -> ResponseMessageType:
    if not data_access.has_user(user_id):
        logging.warning("No user data existing: %s", user_id)
        return ("no_user", {})
    user_data = data_access.get_user_info(user_id)
    if product_id not in user_data.product_tracking:
        logging.warning("User tried to delete untracked item.")
        return ("not_tracking", {})
    return _delete_tracking_product(user_data, product_id)


def _delete_tracking_product(user: User, product_id: str) -> ResponseMessageType:
    try:
        user.product_tracking.remove(product_id)
        user.count_tracking = len(user.product_tracking)
        data_access.update_user(user)
        return ("deleted", {})
    except DatabaseOperationError:
        logging.exception("Delete item error.")
    return ("internal_error", {})


async def list_tracking_products(user_id: str) -> ResponseMessageType:
    # Retrieve usre data
    if not data_access.has_user(user_id):
        logging.info("No user %s data.", user_id)
        return ("no_user", {})
    user_data = data_access.get_user_info(user_id)
    # Fetch all items being tracked.
    logging.debug(
        "User %s's following items:\n%s", user_data.user_id, user_data.product_tracking
    )
    if not user_data.product_tracking:
        logging.info("User %s has no tracking item.", user_id)
        return ("no_item", {})
    return (
        "following",
        (await compose_product_carousel(user_data.product_tracking)).dict(
            exclude_none=True
        ),
    )
