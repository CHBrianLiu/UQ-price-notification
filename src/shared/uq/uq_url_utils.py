class UqProductCodeParser:
    _url: str

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
        pass
