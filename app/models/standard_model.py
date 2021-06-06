from abc import ABCMeta, abstractmethod
from typing import List

from app.models.Product import Product
from app.models.User import User


class IDataStore(metaclass=ABCMeta):
    @abstractmethod
    def has_user(self, user_id: str) -> bool:
        pass

    @abstractmethod
    def get_user_info(self, user_id: str) -> User:
        pass

    @abstractmethod
    def update_user(self, user: User):
        pass

    @abstractmethod
    def is_product_tracked_by_any_user(self, product_id: str) -> bool:
        pass

    @abstractmethod
    def get_product_info(self, product_id: str) -> Product:
        pass

    @abstractmethod
    def update_product(self, product: Product):
        pass

    @abstractmethod
    def get_all_user_ids(self) -> List[str]:
        pass

    @abstractmethod
    def get_all_tracked_product_ids(self) -> List[str]:
        pass

    @abstractmethod
    def get_all_price_down_product_ids(self) -> List[str]:
        pass

    @abstractmethod
    def update_price_down_product_list(self, product_ids: List[str]):
        pass


class DatabaseOperationError(Exception):
    pass
