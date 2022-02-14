import unittest
from unittest import mock

from src.shared.uq.uq_product import UqProduct, UqRetriever, UqProductException


class MockUqRetriever:
    def get_product_info(self):
        return {
            "caseFlag": "Y",
            "isPickup": "N",
            "gDept": "25",
            "taobaoID": "",
            "originPrice": 2990.0,
            "planOnDate": "",
            "isExpress": "N",
            "sales": 0,
            "maxVaryPrice": "",
            "epLimitFlag": "",
            "groupCode": "",
            "productLabel": [],
            "firstListTime": "1623600000000",
            "gDeptValue": "\u5973\u88dd",
            "priceColor": "red",
            "weight": 749.0,
            "subtitle": "",
            "modelHeight": "",
            "name": "UNIQLO PLUS \u91dd\u7e54\u5916\u5957",
            "subtitleUrl": "",
            "epLimitStartTime": "",
            "listYearSeason": "2020\u5e74\u590f\u5b63",
            "code": "431318",
            "isConcessionalRate": "Y",
            "intenCode": "",
            "remark": "",
            "saleDate": "",
            "subTitlePc": "",
            "boxForGift": "",
            "isTimeDoptimal": "N",
            "identity": ["concessional_rate"],
            "isPickupV2": "Y",
            "categories": [],
            "planOutDate": "",
            "minFinalInseam": "",
            "makePantsLengthFlag": "N",
            "isShoesOrSocks": "N",
            "platformUrl": "",
            "introduce": "",
            "sex": "\u5973\u88dd",
            "sizeCategory": "",
            "minVaryPrice": "",
            "fullName": "\u5973\u88dd UNIQLO PLUS \u91dd\u7e54\u5916\u5957 431318",
            "activeTags": "N",
            "isNew": "N",
            "mobileSubtitleUrl": "",
            "modelSize": "",
            "customMadeFlag": "",
            "timeLimitedBegin": "",
            "epLimitEndTime": "",
            "isNoReasonToReturn": "Y",
            "productCode": "u0000000000242",
            "timeLimitedEnd": "",
            "oms_productCode": "431318000",
            "deliveryTemplateId": 7,
            "stylingBook": "",
        }

    def get_price_info(self):
        return {
            "summary": {
                "presaleServiceSwitch": "Y",
                "caseFlag": "Y",
                "originPrice": 2990.0,
                "designScore": 0.0,
                "score": 0.0,
                "inactive": "N",
                "minSize": "S",
                "productLabel": [],
                "evaluationCount": 0,
                "minPrice": 790.0,
                "maxPrice": 790.0,
                "maxSize": "XL",
                "enabledFlag": "Y",
                "currSystemTime": 1642888164435,
                "identity": ["concessional_rate"],
                "makePantsLengthFlag": "N",
                "caseServiceSwitch": "Y",
                "isShoesOrSocks": "N",
                "tailorServiceSwitch": "Y",
                "fabricScore": 0.0,
                "approval": "LIST",
                "label": "concessional_rate",
                "customMadeFlag": "N",
                "productCode": "u0000000000242",
                "sizeScore": 0.0,
                "workmanshipScore": 0.0,
                "levels": [0, 0, 0, 0, 0],
            },
            "stockLevele": [
                {
                    "objectVersionNumber": 1,
                    "lowStock_moreThan": 1,
                    "stockLevelId": "levelId-12587",
                    "highStock_moreThan": 7,
                }
            ],
            "rows": [
                {
                    "productId": "u0000000000242000",
                    "priceType": "VaryPriceGroup",
                    "enabledFlag": "Y",
                    "pantsLength": "",
                    "price": 790.0,
                    "omsSkuCode": "43131866003000",
                    "skuId": 3237,
                },
                {
                    "productId": "u0000000000242001",
                    "priceType": "VaryPriceGroup",
                    "enabledFlag": "Y",
                    "pantsLength": "",
                    "price": 790.0,
                    "omsSkuCode": "43131866004000",
                    "skuId": 3238,
                },
                {
                    "productId": "u0000000000242002",
                    "priceType": "VaryPriceGroup",
                    "enabledFlag": "Y",
                    "pantsLength": "",
                    "price": 790.0,
                    "omsSkuCode": "43131866005000",
                    "skuId": 3239,
                },
                {
                    "productId": "u0000000000242003",
                    "priceType": "VaryPriceGroup",
                    "enabledFlag": "Y",
                    "pantsLength": "",
                    "price": 790.0,
                    "omsSkuCode": "43131866006000",
                    "skuId": 3240,
                },
                {
                    "productId": "u0000000000242004",
                    "priceType": "VaryPriceGroup",
                    "enabledFlag": "Y",
                    "pantsLength": "",
                    "price": 790.0,
                    "omsSkuCode": "43131869003000",
                    "skuId": 3241,
                },
                {
                    "productId": "u0000000000242005",
                    "priceType": "VaryPriceGroup",
                    "enabledFlag": "Y",
                    "pantsLength": "",
                    "price": 790.0,
                    "omsSkuCode": "43131869004000",
                    "skuId": 3242,
                },
                {
                    "productId": "u0000000000242006",
                    "priceType": "VaryPriceGroup",
                    "enabledFlag": "Y",
                    "pantsLength": "",
                    "price": 790.0,
                    "omsSkuCode": "43131869005000",
                    "skuId": 3243,
                },
                {
                    "productId": "u0000000000242007",
                    "priceType": "VaryPriceGroup",
                    "enabledFlag": "Y",
                    "pantsLength": "",
                    "price": 790.0,
                    "omsSkuCode": "43131869006000",
                    "skuId": 3244,
                },
            ],
        }

    def get_image_info(self):
        return {
            "mStorePic": ["/hmall/test/u0000000000242/storeDescription/1.jpg"],
            "video": {},
            "rows": {
                "u0000000000242006": {
                    "skuPic_40": "/hmall/test/u0000000000242/sku/40/COL69.jpg",
                    "skuPic_1000": "/hmall/test/u0000000000242/sku/1000/COL69.jpg",
                    "chipPic_22": "/hmall/test/u0000000000242/chip/22/COL69.jpg",
                    "skuPic_285": "/hmall/test/u0000000000242/sku/285/COL69.jpg",
                    "skuPic_561": "/hmall/test/u0000000000242/sku/561/COL69.jpg",
                },
                "u0000000000242005": {
                    "skuPic_40": "/hmall/test/u0000000000242/sku/40/COL69.jpg",
                    "skuPic_1000": "/hmall/test/u0000000000242/sku/1000/COL69.jpg",
                    "chipPic_22": "/hmall/test/u0000000000242/chip/22/COL69.jpg",
                    "skuPic_285": "/hmall/test/u0000000000242/sku/285/COL69.jpg",
                    "skuPic_561": "/hmall/test/u0000000000242/sku/561/COL69.jpg",
                },
                "u0000000000242004": {
                    "skuPic_40": "/hmall/test/u0000000000242/sku/40/COL69.jpg",
                    "skuPic_1000": "/hmall/test/u0000000000242/sku/1000/COL69.jpg",
                    "chipPic_22": "/hmall/test/u0000000000242/chip/22/COL69.jpg",
                    "skuPic_285": "/hmall/test/u0000000000242/sku/285/COL69.jpg",
                    "skuPic_561": "/hmall/test/u0000000000242/sku/561/COL69.jpg",
                },
                "u0000000000242003": {
                    "skuPic_40": "/hmall/test/u0000000000242/sku/40/COL66.jpg",
                    "skuPic_1000": "/hmall/test/u0000000000242/sku/1000/COL66.jpg",
                    "chipPic_22": "/hmall/test/u0000000000242/chip/22/COL66.jpg",
                    "skuPic_285": "/hmall/test/u0000000000242/sku/285/COL66.jpg",
                    "skuPic_561": "/hmall/test/u0000000000242/sku/561/COL66.jpg",
                },
                "u0000000000242007": {
                    "skuPic_40": "/hmall/test/u0000000000242/sku/40/COL69.jpg",
                    "skuPic_1000": "/hmall/test/u0000000000242/sku/1000/COL69.jpg",
                    "chipPic_22": "/hmall/test/u0000000000242/chip/22/COL69.jpg",
                    "skuPic_285": "/hmall/test/u0000000000242/sku/285/COL69.jpg",
                    "skuPic_561": "/hmall/test/u0000000000242/sku/561/COL69.jpg",
                },
                "u0000000000242002": {
                    "skuPic_40": "/hmall/test/u0000000000242/sku/40/COL66.jpg",
                    "skuPic_1000": "/hmall/test/u0000000000242/sku/1000/COL66.jpg",
                    "chipPic_22": "/hmall/test/u0000000000242/chip/22/COL66.jpg",
                    "skuPic_285": "/hmall/test/u0000000000242/sku/285/COL66.jpg",
                    "skuPic_561": "/hmall/test/u0000000000242/sku/561/COL66.jpg",
                },
                "u0000000000242001": {
                    "skuPic_40": "/hmall/test/u0000000000242/sku/40/COL66.jpg",
                    "skuPic_1000": "/hmall/test/u0000000000242/sku/1000/COL66.jpg",
                    "chipPic_22": "/hmall/test/u0000000000242/chip/22/COL66.jpg",
                    "skuPic_285": "/hmall/test/u0000000000242/sku/285/COL66.jpg",
                    "skuPic_561": "/hmall/test/u0000000000242/sku/561/COL66.jpg",
                },
                "u0000000000242000": {
                    "skuPic_40": "/hmall/test/u0000000000242/sku/40/COL66.jpg",
                    "skuPic_1000": "/hmall/test/u0000000000242/sku/1000/COL66.jpg",
                    "chipPic_22": "/hmall/test/u0000000000242/chip/22/COL66.jpg",
                    "skuPic_285": "/hmall/test/u0000000000242/sku/285/COL66.jpg",
                    "skuPic_561": "/hmall/test/u0000000000242/sku/561/COL66.jpg",
                },
            },
            "modelPicH5": [],
            "colorList": [
                {
                    "chipPic": "/hmall/test/u0000000000242/chip/22/COL66.jpg",
                    "styleText": "66 BLUE",
                    "style": "BLUE",
                    "colorNo": "COL66",
                },
                {
                    "chipPic": "/hmall/test/u0000000000242/chip/22/COL69.jpg",
                    "styleText": "69 NAVY",
                    "style": "NAVY",
                    "colorNo": "COL69",
                },
            ],
            "main561": [
                "/hmall/test/u0000000000242/main/first/561/1.jpg",
                "/hmall/test/u0000000000242/main/other1/480/2.jpg",
                "/hmall/test/u0000000000242/main/other2/480/3.jpg",
                "/hmall/test/u0000000000242/main/other3/480/4.jpg",
                "/hmall/test/u0000000000242/main/other4/480/5.jpg",
                "/hmall/test/u0000000000242/main/other5/480/6.jpg",
                "/hmall/test/u0000000000242/main/other6/480/7.jpg",
                "/hmall/test/u0000000000242/main/other7/480/8.jpg",
                "/hmall/test/u0000000000242/main/other8/480/9.jpg",
                "/hmall/test/u0000000000242/main/other9/480/10.jpg",
                "/hmall/test/u0000000000242/main/other10/480/11.jpg",
                "/hmall/test/u0000000000242/main/other11/480/12.jpg",
                "/hmall/test/u0000000000242/main/other12/480/13.jpg",
                "/hmall/test/u0000000000242/main/other13/480/14.jpg",
            ],
            "mDetailPic": [],
            "productCode": "u0000000000242",
            "modelPicPC": {},
            "main1000": [
                "/hmall/test/u0000000000242/main/first/1000/1.jpg",
                "/hmall/test/u0000000000242/main/other1/1000/2.jpg",
                "/hmall/test/u0000000000242/main/other2/1000/3.jpg",
                "/hmall/test/u0000000000242/main/other3/1000/4.jpg",
                "/hmall/test/u0000000000242/main/other4/1000/5.jpg",
                "/hmall/test/u0000000000242/main/other5/1000/6.jpg",
                "/hmall/test/u0000000000242/main/other6/1000/7.jpg",
                "/hmall/test/u0000000000242/main/other7/1000/8.jpg",
                "/hmall/test/u0000000000242/main/other8/1000/9.jpg",
                "/hmall/test/u0000000000242/main/other9/1000/10.jpg",
                "/hmall/test/u0000000000242/main/other10/1000/11.jpg",
                "/hmall/test/u0000000000242/main/other11/1000/12.jpg",
                "/hmall/test/u0000000000242/main/other12/1000/13.jpg",
                "/hmall/test/u0000000000242/main/other13/1000/14.jpg",
            ],
            "main80": [
                "/hmall/test/u0000000000242/main/first/80/1.jpg",
                "/hmall/test/u0000000000242/main/other1/80/2.jpg",
                "/hmall/test/u0000000000242/main/other2/80/3.jpg",
                "/hmall/test/u0000000000242/main/other3/80/4.jpg",
                "/hmall/test/u0000000000242/main/other4/80/5.jpg",
                "/hmall/test/u0000000000242/main/other5/80/6.jpg",
                "/hmall/test/u0000000000242/main/other6/80/7.jpg",
                "/hmall/test/u0000000000242/main/other7/80/8.jpg",
                "/hmall/test/u0000000000242/main/other8/80/9.jpg",
                "/hmall/test/u0000000000242/main/other9/80/10.jpg",
                "/hmall/test/u0000000000242/main/other10/80/11.jpg",
                "/hmall/test/u0000000000242/main/other11/80/12.jpg",
                "/hmall/test/u0000000000242/main/other12/80/13.jpg",
                "/hmall/test/u0000000000242/main/other13/80/14.jpg",
            ],
            "semi": {},
            "detailPic": [],
            "mMeasurementPic": ["/hmall/test/u0000000000242/measurement/1.jpg"],
        }


class TestUqRetriever(unittest.TestCase):
    def test_get_product_info_should_use_product_spu_url(self):
        session = mock.MagicMock()

        retriever = UqRetriever("product_code", session)
        retriever.get_product_info()

        session.get.assert_called_once_with(
            "https://www.uniqlo.com/tw/data/products/spu/zh_TW/product_code.json",
            headers=retriever._custom_headers,
        )

    def test_get_price_info_should_use_product_spu_pc_query_url(self):
        session = mock.MagicMock()

        retriever = UqRetriever("product_code", session)
        retriever.get_price_info()

        session.get.assert_called_once_with(
            "https://d.uniqlo.com/tw/p/product/i/product/spu/pc/query/product_code/zh_TW",
            headers=retriever._custom_headers,
        )

    def test_get_image_info_with_correct_url(self):
        session = mock.MagicMock()

        retriever = UqRetriever("u0000000000242", session)
        retriever.get_image_info()

        session.get.assert_called_once_with(
            "https://www.uniqlo.com/tw/data/products/zh_TW/u0000000000242.json",
            headers=retriever._custom_headers,
        )

    def test_get_product_info_should_raise_uq_product_exception_when_request_not_succeeded(
        self,
    ):
        session = mock.MagicMock()
        response = mock.MagicMock()
        response.ok = False
        session.get.return_value = response

        retriever = UqRetriever("product_code", session)

        with self.assertRaises(UqProductException):
            retriever.get_product_info()

    def test_get_price_info_should_raise_uq_product_exception_when_request_not_succeeded(
        self,
    ):
        session = mock.MagicMock()
        response = mock.MagicMock()
        response.ok = False
        session.get.return_value = response

        retriever = UqRetriever("product_code", session)

        with self.assertRaises(UqProductException):
            retriever.get_price_info()

    def test_get_image_info_should_raise_uq_product_exception_when_request_not_succeeded(
        self,
    ):
        session = mock.MagicMock()
        response = mock.MagicMock()
        response.ok = False
        session.get.return_value = response

        retriever = UqRetriever("product_code", session)

        with self.assertRaises(UqProductException):
            retriever.get_image_info()


class TestUqProduct(unittest.TestCase):
    def test_uq_product_to_get_correct_product_name(self):
        retriever = MockUqRetriever()
        item = UqProduct(retriever)
        self.assertEqual("女裝 UNIQLO PLUS 針織外套 431318", item.name)

    def test_uq_product_to_get_correct_product_original_price(self):
        retriever = MockUqRetriever()
        item = UqProduct(retriever)
        self.assertEqual(2990, item.original_price)

    def test_uq_product_to_get_correct_product_special_offer(self):
        retriever = MockUqRetriever()
        item = UqProduct(retriever)
        self.assertEqual(790, item.special_offer)

    def test_uq_product_to_get_correct_product_is_on_sale(self):
        retriever = MockUqRetriever()
        item = UqProduct(retriever)
        self.assertEqual(True, item.is_on_sale)

    def test_uq_product_to_get_correct_product_code(self):
        retriever = MockUqRetriever()
        item = UqProduct(retriever)
        self.assertEqual("u0000000000242", item.product_code)

    def test_uq_product_to_get_correct_product_url(self):
        retriever = MockUqRetriever()
        item = UqProduct(retriever)
        self.assertEqual(
            "https://www.uniqlo.com/tw/zh_TW/product-detail.html?productCode=u0000000000242",
            item.website_url,
        )

    def test_uq_product_to_get_correct_image_url(self):
        retriever = MockUqRetriever()
        item = UqProduct(retriever)
        self.assertEqual(
            "https://www.uniqlo.com/tw/hmall/test/u0000000000242/main/first/561/1.jpg",
            item.image_url,
        )
