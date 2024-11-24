from django.urls import path
from app.crawler.views import YodyCategoryETLView, YodyProductExtractView, DAGTriggerYodyProductView

app_name = "crawler"

urlpatterns = [
    path("etl/yody-category/", YodyCategoryETLView.as_view(), name="yody-category-etl"),
    path("extract/yody-product-to-minio/", YodyProductExtractView.as_view(), name="yody-product-extract"),
    path("trigger/yody-product-to-kafka/", DAGTriggerYodyProductView.as_view(), name="yody-product-trigger"),
]
