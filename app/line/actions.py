import logging
from typing import Any, Dict

from app.config import app_config
from app.line.messages import (
    ButtonTemplateMessage,
    MessageAction,
    PostbackAction,
    TemplateMessage,
)
from app.line.postback_data import PostbackDataAdding
from app.line.reply_messages import ResponseMessageType
from app.line.utils import compose_product_carousel
from app.models.data_store import data_access
from app.uq.product import NoUqProduct, UqProduct


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
    add_action_button = PostbackAction(
        label="Yes",
        displayText="Yes",
        data=PostbackDataAdding(
            product_id=product.product_id, product_name=product.product_name
        ).json(),
    )
    cancel_action_button = MessageAction(text="No", label="No")
    return ButtonTemplateMessage(
        title=product.product_name,
        text=f"{app_config.UQ_PRODUCT_CURRENCY}{product.product_derivatives_lowest_price}\n你要追蹤此商品嗎？",
        thumbnailImageUrl=product.product_image_url,
        actions=[add_action_button, cancel_action_button],
    )


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
