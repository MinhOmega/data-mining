from django.urls import path
from app.crawler.views import YodyCategoryETLView, YodyProductExtractView, YodyProductLoadView, TriggerYodyConsumerView

app_name = "crawler"

urlpatterns = [
    path("etl/yody-category/", YodyCategoryETLView.as_view(), name="yody-category-etl"),
    path("etl/yody-product/", YodyProductExtractView.as_view(), name="yody-product-extract"),
    path("load/yody-product/", YodyProductLoadView.as_view(), name="yody-product-load"),
    path("trigger/yody-consumer/", TriggerYodyConsumerView.as_view(), name="yody-consumer-trigger"),
]
