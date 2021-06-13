from typing import List

from app.config import app_config
from app.line.messages import (
    CarouselTemplateColumn,
    CarouselTemplateImageRatio,
    CarouselTemplateMessage,
    MessageAction,
    TemplateMessage,
    UriAction,
)
from app.uq.product import UqProduct


async def compose_product_carousel(product_ids: List[str]) -> TemplateMessage:
    carousel_template = CarouselTemplateMessage(
        columns=[
            create_uq_product_carousel_template_column(
                await UqProduct.create(product_id)
            )
            for product_id in product_ids
        ],
        imageAspectRatio=CarouselTemplateImageRatio.square,
    )
    alt_text = "\n".join(
        [
            f"{app_config.UQ_PRODUCT_URL_PREFIX}{product_id}"
            for product_id in product_ids
        ]
    )
    return TemplateMessage(altText=alt_text, template=carousel_template)


def create_uq_product_carousel_template_column(
    product: UqProduct,
) -> CarouselTemplateColumn:
    item_link_action_button = UriAction(uri=product.product_url, label="前往商品頁面")
    delete_item_action_button = MessageAction(
        text=f"delete {product.product_id}", label="取消追蹤商品"
    )
    return CarouselTemplateColumn(
        title=product.product_name,
        text=f"{app_config.UQ_PRODUCT_CURRENCY}{product.product_derivatives_lowest_price}",
        thumbnailImageUrl=product.product_image_url,
        actions=[item_link_action_button, delete_item_action_button],
    )
