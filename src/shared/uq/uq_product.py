import requests


class UqProductException(Exception):
    pass


class UqRetriever:
    def __init__(self, product_code: str) -> None:
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

    def _get_data_from_url(self, url) -> dict:
        headers = {
            "User-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
        }
        try:
            resp = self._session.get(url, headers=self._custom_headers)
            if not resp.ok:
                raise UqProductException()
            return resp.json()
        except requests.exceptions.JSONDecodeError as e:
            raise UqProductException() from e

    def get_product_info(self) -> dict:
        try:
            data = self._get_data_impl(self._product_info_url)
            return data["summary"]
        except KeyError as e:
            raise UqProductException() from e

    def get_price_info(self) -> dict:
        try:
            data = self._get_data_impl(self._price_info_url)
            return data["resp"][0]
        except KeyError as e:
            raise UqProductException() from e


class UqProduct:
    _price_data: dict = None
    _product_data: dict = None

    def __init__(self, retriever: UqRetriever) -> None:
        self.retriever = retriever

    @property
    def name(self) -> str:
        if not self._product_data:
            self._product_data = self.retriever.get_product_info()
        try:
            return self._product_data["fullName"]
        except KeyError as e:
            raise UqProductException() from e

    @property
    def is_on_sale(self) -> bool:
        if not self._product_data:
            self._product_data = self.retriever.get_product_info()
        try:
            return (
                self._product_data["priceColor"] == "red"
                and self.special_offer < self.original_price
            )
        except KeyError as e:
            raise UqProductException() from e

    @property
    def original_price(self) -> int:
        if not self._product_data:
            self._product_data = self.retriever.get_product_info()
        try:
            return int(self._product_data["originPrice"])
        except KeyError as e:
            raise UqProductException() from e

    @property
    def special_offer(self) -> int:
        if not self._price_data:
            self._price_data = self.retriever.get_price_info()
        try:
            min_price: int = self._price_data["summary"]["minPrice"]
            max_price: int = self._price_data["summary"]["maxPrice"]
            if min_price != max_price:
                # handle the min price and max price are different
                pass
            return int(min_price)
        except KeyError as e:
            raise UqProductException() from e
