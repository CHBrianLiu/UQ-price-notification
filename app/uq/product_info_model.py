from pydantic import BaseModel
from typing import Dict


class L2GoodsInfo(BaseModel):
    l2GoodsCd: str
    itemCd: str
    salesPrice: str
    cSalesPrice: int
    firstPriceUseFlg: bool
    roughEstimatePrice: str
    discountFlg: bool
    termLimitSalesFlg: bool
    termLimitSalesEndMsg: str
    maxLength: int
    minAlterationLength: int
    inseamReqCostFlg: bool
    realStockCnt: int
    sumStockCnt: int
    lowStockFlg: bool
    colorCd: str
    sizeCd: str
    lengthCd: str
    newFlg: bool
    promoId: str
    promoNm: str
    promoShortComment: str
    promoRuleInfo: str


class L2GoodsList(BaseModel):
    L2GoodsInfo: L2GoodsInfo


class Goods(BaseModel):
    subMessages: Dict[str, str]
    l1GoodsCd: int
    brandCd: int
    firstPrice: str
    cFirstPrice: str
    lengthDiv: int
    specialSizeFlg: int
    onlineLimitFlg: int
    alterationFlag: int
    dispL2GoodsKey: str
    goodsNm: str
    shortComment: str
    handlingInfo: str
    materialInfo: str
    dtlExp: str
    mobileShortComment: str
    mobileHandlingInfo: str
    mobileMaterialInfo: str
    mobileDltExp: str
    funcGroupIcon1Name: str
    funcGroupIcon1Detail: str
    funcGroupIcon2Name: str
    funcGroupIcon2Detail: str
    funcGroupIcon3Name: str
    funcGroupIcon3Detail: str
    alterationUnit: int
    alterationUnitNm: str
    alterationMinLength: int
    alterationDoubleWidth: int
    chipUnit: str
    httpImgDomain: str
    httpsImgDomain: str
    mbHttpImgDomain: str
    mbHttpsImgDomain: str
    goodsSubImageList: str
    stockCntL1: int
    dispCd: str
    dispClassifCd: int
    l2GoodsList: Dict[str, L2GoodsList]
    colorInfoList: Dict[str, str]
    sizeInfoList: Dict[str, str]
    lengthInfoList: Dict[str, str]


class Detail(BaseModel):
    resultCode: str
    messageCode: str
    message: str


class ResponseInfo(BaseModel):
    site: str
    resultCode: str
    message: str
    detail: Detail


class GoodsInfo(BaseModel):
    responseInfo: ResponseInfo
    goods: Goods


class UqProductData(BaseModel):
    GoodsInfo: GoodsInfo
