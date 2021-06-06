import logging
from typing import List

from app.config import app_config
from app.line.reply_messages import ResponseMessageType
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

    # check if product is on-sale
    if product.is_product_on_sale:
        return ("on_sale", {"title": product.product_name})

    # Mew user, copy from template
    user_data = (
        data_access.get_user_info(user_id)
        if data_access.has_user(user_id)
        else User(user_id=user_id, count_tracking=0, product_tracking=[])
    )

    # Product has been tracked
    if product_id in user_data.product_tracking:
        return ("in_list", {"title": product.product_name})
    user_data.product_tracking.add(product_id)
    user_data.count_tracking += 1

    # Create product
    if not data_access.is_product_tracked_by_any_user(product_id):
        data_access.update_product(Product(product_id=product_id))

    # update user record
    data_access.update_user(user_data)

    return ("tracking", {"title": product.product_name})


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


def list_tracking_products(user_id: str) -> ResponseMessageType:
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
        {"products": _compose_product_list_message(user_data.product_tracking)},
    )


def _compose_product_list_message(products: List[str]):
    return "\n".join(
        [f"{app_config.UQ_PRODUCT_URL_PREFIX}{product_id}" for product_id in products]
    )
