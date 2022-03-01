from src.shared.db.models import User, Product, UserProduct


class UserDataRetriever:
    _user: User

    def __init__(self, user: User):
        self._user = user

    def get_subscribed_products(self) -> dict[str, Product]:
        products = (
            Product.select()
            .join(UserProduct)
            .join(User)
            .where(User.id == self._user.id)
        )
        return {product.product_code: product for product in products}
