import asyncio
import logging
from typing import List

from app.config import app_config
from app.line.push import push_price_down_message
from app.models.data_store import data_access
from app.uq.product import UqProduct


async def check_pricing():
    # get all product
    products = data_access.get_all_tracked_product_ids()
    on_sale_products = []

    await asyncio.gather(
        *[
            _append_on_sale_product(product_id, on_sale_products)
            for product_id in products
        ]
    )

    logging.debug("Products on-sale: %s", on_sale_products)
    data_access.update_price_down_product_list(on_sale_products)


async def notify():
    users = data_access.get_all_user_ids()
    on_sale_products = data_access.get_all_price_down_product_ids()

    await asyncio.gather(
        *[_notify_one_user(user_id, on_sale_products) for user_id in users]
    )
    # TODO: delete product record


async def _append_on_sale_product(product_id: str, products: List[str]):
    product = await UqProduct.create(product_id)
    if product.is_product_on_sale:
        products.append(product_id)


async def _notify_one_user(user_id: str, target_products: List[str]):
    user_data = data_access.get_user_info(user_id)
    user_tracking_list = user_data.product_tracking
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
    user_data.product_tracking = user_tracking_list - products_to_notify
    user_data.count_tracking = len(user_data.product_tracking)
    data_access.update_user(user_data)
