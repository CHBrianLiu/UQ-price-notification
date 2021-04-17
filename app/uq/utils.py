import logging
from aiohttp import http
from bs4 import BeautifulSoup
import aiohttp

from app.config.loader import get_config_by_key


UQ_URL_PREFIX = get_config_by_key("uq.product_url_prefix")


async def get_product_page(product_id: str) -> str:
    full_url = f"{UQ_URL_PREFIX}{product_id}"
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


def get_product_name(content: str):
    soup = BeautifulSoup(content, 'html.parser')
    return soup.find(lambda tag: tag.has_attr('id') and tag['id'] == 'goodsNmArea').text
