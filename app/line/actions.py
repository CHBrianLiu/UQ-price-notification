import json
from copy import deepcopy
from typing import Any, Dict, Tuple

from app.models import azure_storage_blob
from app.models.templates import users
from app.uq.product import UqProduct


async def add_tracking_product(
    user_id: str, product_id: str
) -> Tuple[str, Dict[str, Any]]:
    product = await UqProduct.create(product_id)

    if product.page is None:
        return ("not_found", {})

    # check if product is on-sale
    if await product.is_product_on_sale():
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
