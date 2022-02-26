from typing import Callable

import requests


class UqProductException(Exception):
    pass


class UqRetriever:
    """
    The class to get the UQ product information from the website.
    """

    # The user-agent header matters when issue an API request to the server
    _custom_headers = {
        "User-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) \
                AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    }

    def __init__(self, product_code: str, session: requests.Session) -> None:
        self.product_code = product_code
        self._session = session

    @property
    def _product_info_url(self) -> str:
        domain = "www.uniqlo.com"
        path = f"/tw/data/products/spu/zh_TW/{self.product_code}.json"
        return f"https://{domain}{path}"

    @property
    def _price_info_url(self) -> str:
        domain = "d.uniqlo.com"
        path = f"/tw/p/product/i/product/spu/pc/query/{self.product_code}/zh_TW"
        return f"https://{domain}{path}"

    @property
    def _image_info_url(self) -> str:
        domain = "www.uniqlo.com"
        path = f"/tw/data/products/zh_TW/{self.product_code}.json"
        return f"https://{domain}{path}"

    def _get_data_from_url(self, url) -> dict:
        try:
            resp = self._session.get(url, headers=self._custom_headers)
            if not resp.ok:
                raise UqProductException()
            return resp.json()
        except requests.exceptions.JSONDecodeError as e:
            raise UqProductException() from e

    def get_product_info(self) -> dict:
        """
        Get the UQ product information from the website, including name, description and so on.

        Returns: A dictionary containing the production information. Sample data can be found in
                 tests/ut/shared/uq/test_uq_product.py.
        """
        try:
            data = self._get_data_from_url(self._product_info_url)
            return data["summary"]
        except KeyError as e:
            raise UqProductException() from e

    def get_price_info(self) -> dict:
        """
        Get the UQ product price information from the website.

        Returns: A dictionary containing the production information. Sample data can be found in
                 tests/ut/shared/uq/test_uq_product.py.
        """
        try:
            data = self._get_data_from_url(self._price_info_url)
            return data["resp"][0]
        except KeyError as e:
            raise UqProductException() from e

    def get_image_info(self) -> dict:
        """
        Get the UQ product image url information from the website

        Returns: A dictionary containing the image url information. Sample data can be found in
                 tests/ut/shared/uq/test_uq_product.py.
        """
        try:
            data = self._get_data_from_url(self._image_info_url)
            return data
        except KeyError as e:
            raise UqProductException() from e


class UqProduct:
    """
    A data model that represents a product. The data is loaded when it's required.
    """

    _price_data: dict

    _product_data: dict

    _image_data: dict

    def __init__(self, retriever: UqRetriever) -> None:
        self.retriever = retriever

    def _require(self=None, *, field: str, populater: str):
        """
        As the data in this class is lazily loaded, we need to retrieve required data
        before using it. This decorator can help simplify the code by specifying the
        required data property and the method of UqRetriever to populate the data.
        Args:
            field: The required field.
            populater: The method name from the UqRetriever to get the data.

        Returns: decorator
        """

        def deco(f: Callable):
            def wrapper(self: "UqProduct", *args, **kwargs):
                if not hasattr(self, field) or getattr(self, field) is None:
                    data = getattr(self.retriever, populater)()
                    setattr(self, field, data)
                return f(self, *args, **kwargs)

            return wrapper

        return deco

    @property
    @_require(field="_product_data", populater="get_product_info")
    def name(self) -> str:
        try:
            return self._product_data["fullName"]
        except KeyError as e:
            raise UqProductException() from e

    @property
    def is_on_sale(self) -> bool:
        return self.special_offer < self.original_price

    @property
    @_require(field="_product_data", populater="get_product_info")
    def original_price(self) -> int:
        try:
            return int(self._product_data["originPrice"])
        except KeyError as e:
            raise UqProductException() from e

    @property
    @_require(field="_price_data", populater="get_price_info")
    def special_offer(self) -> int:
        try:
            min_price: int = self._price_data["summary"]["minPrice"]
            return int(min_price)
        except KeyError as e:
            raise UqProductException() from e

    @property
    @_require(field="_product_data", populater="get_product_info")
    def product_code(self) -> str:
        try:
            return self._product_data["productCode"]
        except KeyError as e:
            raise UqProductException() from e

    @property
    def website_url(self) -> str:
        return f"https://www.uniqlo.com/tw/zh_TW/product-detail.html?productCode={self.product_code}"

    @property
    @_require(field="_image_data", populater="get_image_info")
    def image_url(self) -> str:
        try:
            path = self._image_data["main561"][0]
            return f"https://www.uniqlo.com/tw{path}"
        except (KeyError, IndexError) as e:
            raise UqProductException() from e
