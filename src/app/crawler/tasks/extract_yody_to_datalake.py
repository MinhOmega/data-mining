from celery import shared_task

from app.crawler.partners.yody.extract import ExtractYodyProduct
from app.crawler.loaders import YodyProductLoader


class YodyProductCrawler:
    # @shared_task
    def run_extract(self, status: str):
        extractor = ExtractYodyProduct(status=status)
        for _ in extractor.execute():
            pass  # Extractor already saves data to MinIO