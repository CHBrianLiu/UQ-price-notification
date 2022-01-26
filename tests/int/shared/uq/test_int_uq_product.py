import unittest

import requests

from src.shared.uq.uq_product import UqProduct, UqRetriever


class TestIntUqRetriever(unittest.TestCase):
    def test_retrieve_uq_product_name_from_website(self):
        with requests.Session() as session:
            # long-live product
            retriever = UqRetriever("u0000000012397", session)

            product = UqProduct(retriever)

            self.assertEqual("男裝 圓領T恤(短袖) 433025", product.name)

    def test_retrieve_uq_product_original_price_from_website(self):
        with requests.Session() as session:
            # long-live product
            retriever = UqRetriever("u0000000012397", session)

            product = UqProduct(retriever)

            self.assertEqual(190, product.original_price)
