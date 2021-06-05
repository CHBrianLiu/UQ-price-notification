import json
import logging
from copy import deepcopy
from typing import Any, Dict, List, Tuple

from app.config import app_config
from app.line.reply_messages import ResponseMessageType
from app.models import azure_storage_blob
from app.models.templates import users
from app.uq.product import UqProduct, NoUqProduct


async def add_tracking_product(user_id: str, product_id: str) -> ResponseMessageType:
    try:
        product = await UqProduct.create(product_id)
    except NoUqProduct:
        logging.warning("Product ID invalid: %s", product_id)
        return ("not_found", {})

    # check if product is on-sale
    if await product.is_product_on_sale:
        return ("on_sale", {"title": product.product_name})

    # Get user record
    user_container = "users"
    user_record = f"{user_id}.json"

    # Mew user, copy from template
    if not azure_storage_blob.does_file_exist(user_container, user_record):
        user_record_content = deepcopy(users.template)
        user_record_content["user_id"] = user_id
    else:
        user_record_content = json.loads(
            azure_storage_blob.get_file_from_container(user_container, user_record)
        )

    # Product has been tracked
    if product_id in user_record_content["product_tracking"]:
        return ("in_list", {"title": product.product_name})
    user_record_content["product_tracking"] += [product_id]
    user_record_content["count_tracking"] += 1

    # Create product
    product_container = "products"
    product_record = f"{product_id}.json"
    if not azure_storage_blob.does_file_exist(product_container, product_record):
        azure_storage_blob.upload_file_to_container(
            product_container, product_record, ""
        )

    # update user record
    azure_storage_blob.upload_file_to_container(
        user_container, user_record, json.dumps(user_record_content)
    )

    return ("tracking", {"title": product.product_name})


def list_tracking_products(user_id: str) -> ResponseMessageType:
    # Retrieve usre data
    user_record = azure_storage_blob.container_client_factory.get(
        "users"
    ).get_blob_client(f"{user_id}.json")
    if not user_record.exists():
        logging.info("No user %s data.", user_id)
        return ("no_user", {})
    # Fetch all items being tracked.
    user_data = json.loads(user_record.download_blob().content_as_text())
    tracking_items = user_data.get("product_tracking", [])
    logging.debug("User %s's following items:\n%s", user_id, tracking_items)
    if not tracking_items:
        logging.info("User %s has no tracking item.", user_id)
        return ("no_item", {})
    return (
        "following",
        {"products": _compose_product_list_message(tracking_items)},
    )


def _compose_product_list_message(products: List[str]):
    return "\n".join(
        [f"{app_config.UQ_PRODUCT_URL_PREFIX}{product_id}" for product_id in products]
    )
