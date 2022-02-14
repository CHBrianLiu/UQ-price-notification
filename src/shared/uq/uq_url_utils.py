import re


class UqProductCodeParser:
    """
    A class with can parse product code from UNIQLO url
    """

    def __init__(self):
        self.pattern = re.compile(r"u[0-9]+")

    def get_product_code_from_url(self, url: str) -> str | None:
        """
        Both desktop and mobile version urls are supported.
        Desktop url
        https://www.uniqlo.com/tw/zh_TW/product-detail.html?productCode=u0000000009993
        Mobile url
        https://m.uniqlo.com/tw/product?pid=u0000000009993
        """
        match = self.pattern.search(url)
        return match.group() if match else None
