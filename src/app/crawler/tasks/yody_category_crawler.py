from celery import shared_task

from app.core.models.base import Category

from app.crawler.partners.yody.transform import TransformYodyCategory
from app.crawler.partners.yody.extract import ExtractYodyCategory
from app.crawler.partners.yody.load import LoadCategoryData


class YodyCategoryCrawler:
    @shared_task
    def run_etl(self, extract: ExtractYodyCategory, transform: TransformYodyCategory, load: LoadCategoryData) -> list[Category]:
        categories: list[Category] = []
        for raw_datas in extract.execute():
            transformed_data = transform.execute(raw_datas)
            for category in transformed_data:
                categories.append(load.execute(category))

        return categories
    
