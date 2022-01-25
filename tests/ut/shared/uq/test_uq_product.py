import unittest
from src.shared.uq.uq_product import UqProduct


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


class TestUqProduct(unittest.TestCase):
    def test_uq_product_to_get_correct_product_name(self):
        retriever = MockUqRetriever()
        item = UqProduct(retriever)
        self.assertEqual(item.name, "女裝 UNIQLO PLUS 針織外套 431318")

    def test_uq_product_to_get_correct_product_original_price(self):
        retriever = MockUqRetriever()
        item = UqProduct(retriever)
        self.assertEqual(item.original_price, 2990)

    def test_uq_product_to_get_correct_product_special_offer(self):
        retriever = MockUqRetriever()
        item = UqProduct(retriever)
        self.assertEqual(item.special_offer, 790)

    def test_uq_product_to_get_correct_product_is_on_sale(self):
        retriever = MockUqRetriever()
        item = UqProduct(retriever)
        self.assertEqual(item.is_on_sale, True)
