from typing import List

from app.config import app_config
from app.line.messages import (
    CarouselTemplateColumn,
    CarouselTemplateImageRatio,
    CarouselTemplateMessage,
    PostbackAction,
    TemplateMessage,
    UriAction,
)
from app.line.postback_data import PostbackDataDeleting
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
    item_link_action_button = UriAction(uri=product.product_url, label="前往官網")
    delete_item_action_button = PostbackAction(
        displayText="取消追蹤",
        label="取消追蹤",
        data=PostbackDataDeleting(product_id=product.product_id).json(),
    )
    return CarouselTemplateColumn(
        title=product.product_name,
        text=f"{app_config.UQ_PRODUCT_CURRENCY}{product.product_derivatives_lowest_price}",
        thumbnailImageUrl=product.product_image_url,
        actions=[item_link_action_button, delete_item_action_button],
    )
