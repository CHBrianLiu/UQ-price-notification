import logging
from typing import List

import aiohttp
from requests_html import HTML
from app.requests_html_cxt_mgr.session import AsyncHTMLSessionCxt
from app.config import app_config


class UqProduct:
    UQ_URL_PREFIX: str = app_config.UQ_PRODUCT_URL_PREFIX
    PRODUCT_NAME_CSS_SELECTOR: str = app_config.UQ_PRODUCT_NAME_CSS
    PRODUCT_ICON_LIST_CSS_SELECTOR: str = app_config.UQ_ICON_LIST_CSS
    ON_SALE_ICONS: List[str] = app_config.UQ_ON_SALE_ICON_CSS_LIST
    HIDDEN_ICON_STYLE: str = app_config.UQ_HIDE_ICON_STYLE

    product_id: str
    page: str

    @classmethod
    async def create(cls, product_id):
        self = UqProduct(product_id)
        self.page = await self._get_product_page()
        return self

    def __init__(self, product_id: str) -> None:
        self.product_id = product_id

    async def _get_product_page(self):
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
        doc = HTML(html=self.page)
        element = doc.find(self.PRODUCT_NAME_CSS_SELECTOR, first=True)
        if element is None:
            logging.error("Can't find product name from the page.")
            raise RuntimeError("No product name")
        return element.text

    async def is_product_on_sale(self):
        async with AsyncHTMLSessionCxt() as session:
            doc = HTML(session=session, html=self.page)
            await doc.arender()
            icon_list = doc.find(self.PRODUCT_ICON_LIST_CSS_SELECTOR, first=True)
            if icon_list is None:
                logging.error("Can't find icon list from the page.")
                raise RuntimeError("No icon list")
            for icon in self.ON_SALE_ICONS:
                icon_element = icon_list.find(icon, first=True)
                if icon_element is None:
                    logging.warning("Can't find %s icon from the page.")
                    continue
                if icon_element.attrs.get("style", "") != self.HIDDEN_ICON_STYLE:
                    logging.debug(
                        "%s icon found and not hidden.",
                        icon_element.attrs.get("title", ""),
                    )
                    return True
            logging.debug("No on-sale icon shown on page.")
            return False
