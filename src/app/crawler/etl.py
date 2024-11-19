import abc
from typing import Generator, Union
from app.core.models.base import (
    Product, Category, ProductAsset, ProductColor, \
    ProductSize, FactProductDetail,
)


class Extract(metaclass=abc.ABCMeta):
    def execute(self) -> Generator:
        raise NotImplementedError('Not implemented execute() method')
    

class Transform(metaclass=abc.ABCMeta):
    def execute(self, raw_datas: list[dict]) -> list[Union[
        Product, Category, ProductAsset, ProductColor, ProductSize, FactProductDetail
    ]]:
        raise NotImplementedError('Not implemented execute() method')
    

class Load(metaclass=abc.ABCMeta):
    def execute(self, load_datas: list):
        raise NotImplementedError('Not implemented execute() method')