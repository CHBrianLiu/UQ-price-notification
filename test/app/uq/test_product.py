import asyncio
import os
import pathlib
from unittest import TestCase
from unittest.mock import AsyncMock, patch

from app.uq import product


class TestUqProductCreation(TestCase):

    asset_folder_path = os.path.join(os.path.dirname(__file__), "test_assets")

    @patch("aiohttp.ClientSession.get")
    def test_uq_product_create_with_exact_product_code(self, mock_get: AsyncMock):
        item_source_path = os.path.join(self.asset_folder_path, "uq_item_437191.html")
        item_source = pathlib.Path(item_source_path).read_text()
        mock_get.return_value.__aenter__.return_value.ok = True
        mock_get.return_value.__aenter__.return_value.text.return_value = item_source
        created_product = asyncio.run(product.UqProduct.create("437191"))
        self.assertEqual(created_product.product_id, "437191")
        self.assertEqual(created_product.page, item_source)

    @patch("aiohttp.ClientSession.get")
    def test_uq_product_create_with_inexisting_product_code(self, mock_get: AsyncMock):
        item_source_path = os.path.join(
            self.asset_folder_path, "uq_product_not_found.html"
        )
        item_source = pathlib.Path(item_source_path).read_text()
        mock_get.return_value.__aenter__.return_value.ok = True
        mock_get.return_value.__aenter__.return_value.text.return_value = item_source
        with self.assertRaises(product.NoUqProduct):
            asyncio.run(product.UqProduct.create("not_found"))


class TestUqProduct(TestCase):

    asset_folder_path = os.path.join(os.path.dirname(__file__), "test_assets")

    def _page_download_setup(self, mock_get):
        item_source_path = os.path.join(self.asset_folder_path, "uq_item_437191.html")
        item_source = pathlib.Path(item_source_path).read_text()
        mock_get.return_value.__aenter__.return_value.ok = True
        mock_get.return_value.__aenter__.return_value.text.return_value = item_source

    @patch("aiohttp.ClientSession.get")
    def test_uq_product_name(self, mock_get: AsyncMock):
        self._page_download_setup(mock_get)
        created_product = asyncio.run(product.UqProduct.create("437191"))
        self.assertEqual(created_product.product_name, "男裝 可攜式抗UV 連帽外套 (3D剪裁)(印花)")

    @patch("aiohttp.ClientSession.get")
    def test_uq_product_is_on_sale_false(self, mock_get: AsyncMock):
        self._page_download_setup(mock_get)
        created_product = asyncio.run(product.UqProduct.create("437191"))
        self.assertEqual(created_product.is_product_on_sale, False)

    # TODO: current image url extraction method is somehow random.
    # @patch("aiohttp.ClientSession.get")
    # def test_uq_product_product_image_url(self, mock_get: AsyncMock):
    #     pass

    @patch("aiohttp.ClientSession.get")
    def test_uq_product_derivatives_lowest_price(self, mock_get: AsyncMock):
        self._page_download_setup(mock_get)
        created_product = asyncio.run(product.UqProduct.create("437191"))
        self.assertEqual(created_product.product_derivatives_lowest_price, 990)
        
    @patch("aiohttp.ClientSession.get")
    def test_uq_product_url(self, mock_get: AsyncMock):
        self._page_download_setup(mock_get)
        created_product = asyncio.run(product.UqProduct.create("437191"))
        self.assertEqual(created_product.product_url, "https://www.uniqlo.com/tw/store/goods/437191")
