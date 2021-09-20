from unittest import TestCase

from app.line.utils import create_unknown_uq_product_carousel_template_column


class TestCreateUnknownUqProductCarouselTempalteColumn(TestCase):
    def test_create_column(self):
        unknown = create_unknown_uq_product_carousel_template_column("abc")
        self.assertEqual(unknown.title, "不存在的商品 (abc)")
