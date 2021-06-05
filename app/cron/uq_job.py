import asyncio
import json
import logging
from typing import List

from app.config import app_config
from app.line.push import push_price_down_message
from app.models.azure_storage_blob import (
    get_all_products,
    get_all_users,
    get_file_from_container,
    get_price_down_products,
    update_price_down_products,
    upload_file_to_container,
)
from app.uq.product import UqProduct


async def check_pricing():
    # get all product
    products = get_all_products()
    on_sale_products = []

    await asyncio.gather(
        *[
            _append_on_sale_product(product_id, on_sale_products)
            for product_id in products
        ]
    )

    logging.debug("Products on-sale: %s", on_sale_products)
    update_price_down_products(on_sale_products)


async def notify():
    users = get_all_users()
    on_sale_products = get_price_down_products()

    await asyncio.gather(
        *[_notify_one_user(user_id, on_sale_products) for user_id in users]
    )
    # TODO: delete product record


async def _append_on_sale_product(product_id: str, products: List[str]):
    product = await UqProduct.create(product_id)
    if product.is_product_on_sale:
        products.append(product_id)


async def _notify_one_user(user_id: str, target_products: List[str]):
    record_name = f"{user_id}.json"
    user_info = json.loads(get_file_from_container("users", record_name))
    user_tracking_list = set(user_info.get("product_tracking", []))
    target_products = set(target_products)
    products_to_notify = user_tracking_list & target_products
    if not products_to_notify:
        logging.info("For user %s, no tracked product on-sale", user_id)
        return
    await push_price_down_message(
        user_id,
        (
            "price_down",
            {
                "links": "\n".join(
                    [
                        f"{app_config.UQ_PRODUCT_URL_PREFIX}{product_id}"
                        for product_id in products_to_notify
                    ]
                )
            },
        ),
    )
    user_info["product_tracking"] = list(user_tracking_list - products_to_notify)
    upload_file_to_container("users", record_name, json.dumps(user_info))
