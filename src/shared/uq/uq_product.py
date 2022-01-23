import requests


class UqProductException(Exception):
    pass


class UqRetriever:
    def __init__(self, product_code: str) -> None:
        self.product_code = product_code

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

    def _get_data_impl(self, url) -> dict:
        headers = {
            "User-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
        }
        try:
            resp = requests.get(url, headers=headers)
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
        return self._product_data["fullName"]

    @property
    def is_on_sale(self) -> bool:
        if not self._product_data:
            self._product_data = self.retriever.get_product_info()
        return (
            self._product_data["priceColor"] == "red"
            and self.special_offer < self.original_price
        )

    @property
    def original_price(self) -> float:
        if not self._product_data:
            self._product_data = self.retriever.get_product_info()
        return float(self._product_data["originPrice"])

    @property
    def special_offer(self) -> float:
        if not self._price_data:
            self._price_data = self.retriever.get_price_info()
        min_price: float = self._price_data["summary"]["minPrice"]
        max_price: float = self._price_data["summary"]["maxPrice"]
        if min_price != max_price:
            # handle the min price and max price are different
            pass
        return float(min_price)
