import re


class UqProductCodeParser:
    """
    A class with can parse product code from UNIQLO url
    """

    MOBILE_URL_PATTERN = (
        r"^https:\/\/m\.uniqlo\.com\/tw\/product\?.*pid=(?P<code>[A-Z|a-z|0-9]+)"
    )
    DESKTOP_URL_PATTERN = r"^https:\/\/www\.uniqlo\.com\/tw\/zh_TW\/product-detail.html\?.*productCode=(?P<code>[A-Z|a-z|0-9]+)"

    def __init__(self, url: str):
        self._url = url

    def get_product_code_from_url(self) -> str | None:
        """
        Both desktop and mobile version urls are supported.
        Desktop url
        https://www.uniqlo.com/tw/zh_TW/product-detail.html?productCode=u0000000009993
        Mobile url
        https://m.uniqlo.com/tw/product?pid=u0000000009993
        """
        product_code = self._get_product_code_from_desktop_url()
        product_code = product_code or self._get_product_code_from_mobile_url()
        return product_code

    def _get_product_code_from_mobile_url(self) -> str | None:
        result = re.match(self.MOBILE_URL_PATTERN, self._url)
        return result.group("code") if result is not None else None

    def _get_product_code_from_desktop_url(self) -> str | None:
        result = re.match(self.DESKTOP_URL_PATTERN, self._url)
        return result.group("code") if result is not None else None
