import unittest
from src.shared.uq.uq_url_utils import UqProductCodeParser


class TestUqProductCodeParser(unittest.TestCase):
    def test_get_correct_product_code_from_desktop_url(self):
        url = "https://www.uniqlo.com/tw/zh_TW/product-detail.html?productCode=u0000000009993"
        parser = UqProductCodeParser()
        result = parser.get_product_code_from_url(url)
        self.assertEqual(result, "u0000000009993")

    def test_get_correct_product_code_from_mobile_url(self):
        url = "https://m.uniqlo.com/tw/product?pid=u0000000009993"
        parser = UqProductCodeParser()
        result = parser.get_product_code_from_url(url)
        self.assertEqual(result, "u0000000009993")

    def test_get_none_from_a_url_without_product_code(self):
        url = "https://www.uniqlo.com/tw/zh_TW/"
        parser = UqProductCodeParser()
        result = parser.get_product_code_from_url(url)
        self.assertEqual(result, None)

    def test_get_none_from_empty_url(self):
        url = ""
        parser = UqProductCodeParser()
        result = parser.get_product_code_from_url(url)
        self.assertEqual(result, None)

    def test_get_correct_product_code_from_multiple_parameter_url(self):
        url = "https://www.uniqlo.com/tw/zh_TW/product-detail.html?foo=3&productCode=u0000000009993&bar=1"
        parser = UqProductCodeParser()
        result = parser.get_product_code_from_url(url)
        self.assertEqual(result, "u0000000009993")

    def test_get_none_from_non_sense_string(self):
        url = "u1234"
        parser = UqProductCodeParser()
        result = parser.get_product_code_from_url(url)
        self.assertEqual(result, None)
