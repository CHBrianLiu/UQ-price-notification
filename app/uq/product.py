import logging
import re
from typing import List

import aiohttp
from bs4 import BeautifulSoup
from bs4.element import Tag

from app.config import app_config
from app.uq.product_info_model import UqProductData


class UqProduct:
    UQ_URL_PREFIX: str = app_config.UQ_PRODUCT_URL_PREFIX
    JSON_DATA_DECLARATION_REGEX: str = "(var\ +JSON_DATA\ +=\ *)(.*)"

    product_id: str
    page: str
    data: UqProductData
    product_on_sale: bool

    @classmethod
    async def create(cls, product_id: str):
        self = UqProduct(product_id)
        self.page = await self._download_product_page()
        self._record_product_data()
        return self

    def __init__(self, product_id: str) -> None:
        self.product_id = product_id

    async def _download_product_page(self):
        full_url = f"{self.UQ_URL_PREFIX}{self.product_id}"
        async with aiohttp.ClientSession() as session:
            async with session.get(
                full_url,
                timeout=aiohttp.ClientTimeout(total=15),
                headers={
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36 Edg/88.0.705.81"
                },
            ) as response:
                if not response.ok:
                    logging.warning(
                        "Can't access product url: %s with %s code.",
                        full_url,
                        response.status,
                    )
                    return None
                return await response.text()

    @property
    def product_name(self):
        return self.data.GoodsInfo.goods.goodsNm

    @property
    def is_product_on_sale(self) -> bool:
        # Read cache first
        if hasattr(self, "product_on_sale"):
            return self.product_on_sale
        on_sale = False
        for item_info in self.data.GoodsInfo.goods.l2GoodsList.values():
            if (
                item_info.L2GoodsInfo.discountFlg
                or item_info.L2GoodsInfo.termLimitSalesFlg
            ):
                on_sale = True
        # Cache mechanism
        self.product_on_sale = on_sale
        return on_sale

    @property
    def product_image_url(self) -> str:
        # make sure the same image.
        color_options = sorted(self.data.GoodsInfo.goods.colorInfoList.keys())
        return f"{self.data.GoodsInfo.goods.httpsImgDomain}/goods/{self.product_id}/item/{color_options[0]}_{self.product_id}.jpg"

    @property
    def product_derivatives_lowest_price(self) -> int:
        prices = [item.L2GoodsInfo.cSalesPrice for item in self.data.GoodsInfo.goods.l2GoodsList.values()]
        return min(prices)

    @property
    def product_url(self) -> str:
        return f"{self.UQ_URL_PREFIX}{self.product_id}"

    def _record_product_data(self):
        if self.page is None:
            logging.warning("No page content. Cannot process the data retrieval.")
            raise NoUqProduct
        raw_json = self._retrieve_product_data_json_string_from_page()
        if not raw_json:
            logging.warning("No product data found in the page. Stop processing.")
            raise NoUqProduct
        self._parse_product_data_from_raw_json(raw_json)

    def _retrieve_product_data_json_string_from_page(self) -> str:
        html = BeautifulSoup(self.page, "html.parser")
        js_statement_tag = html.find(self._is_uq_json_data_tag)
        if js_statement_tag is None:
            logging.warning("Cannot find the product data from the HTML.")
            return ""
        js_statement = str(js_statement_tag.string)
        regex_pattern = re.compile(self.JSON_DATA_DECLARATION_REGEX)
        # Get rid of the ending semicolon
        return regex_pattern.search(js_statement).group(2)[:-1]

    def _parse_product_data_from_raw_json(self, raw_json: str):
        self.data = UqProductData.parse_raw(raw_json)

    def _is_uq_json_data_tag(self, tag: Tag) -> bool:
        regex_pattern = re.compile(self.JSON_DATA_DECLARATION_REGEX)
        return (
            tag.name == "script"
            and tag.string is not None
            and regex_pattern.search(tag.string) is not None
        )


class NoUqProduct(Exception):
    pass
