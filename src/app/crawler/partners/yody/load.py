from app.crawler import etl
from app.core.models.base import Category


class LoadCategoryData(etl.Load):
    def execute(self, load_data: Category):
        load_data.save()
