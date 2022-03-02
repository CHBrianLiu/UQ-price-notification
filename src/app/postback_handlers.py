import requests

from src.app.postback_dispatcher import PostbackDispatcher
from src.app.postback_handler_base import PostbackHandlerBase
from src.shared.line.postback_action_models import ProductAddingConfirmationDataModel
from src.shared.db.models import User, Product, UserProduct
from src.shared.db.utils import UserDataRetriever
from src.shared.line.message_creators.basic_message_creators import (
    ProductAlreadyInListMessageCreator,
    ProductSuccessfullyAddedMessageCreator,
)
from src.shared.uq.uq_product import UqProduct, UqRetriever

postback_dispatcher = PostbackDispatcher()


@postback_dispatcher.add("add")
class ProductSubscriptionPostbackHandler(PostbackHandlerBase):
    _DATA_MODEL = ProductAddingConfirmationDataModel

    def execute(self):
        (user, _) = User.get_or_create(id=self._source_user_id, role_id=1)

        products = UserDataRetriever(user).get_subscribed_products()
        if self._data.product_code in products:
            product_name = products[self._data.product_code].name
            return ProductAlreadyInListMessageCreator(
                product_name=product_name
            ).generate()

        with requests.Session() as session:
            uq_product = UqProduct(UqRetriever(self._data.product_code, session))
            (product, _) = Product.get_or_create(
                product_code=uq_product.product_code,
                name=uq_product.name,
                current_price=uq_product.special_offer,
                original_price=uq_product.original_price,
                short_description=uq_product.name,
            )

        UserProduct.create(user=user, product=product)

        return ProductSuccessfullyAddedMessageCreator(
            product_name=product.name
        ).generate()
