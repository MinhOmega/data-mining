from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel
from app.core.models.abstract_model import StatusModel

import uuid

# Bảng SourceChannel
class SourceChannel(TimeStampedModel, StatusModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    channel_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

# Bảng Category
class Category(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    source_channel = models.ForeignKey(SourceChannel, on_delete=models.SET_NULL, null=True, blank=True, related_name='category_source_channel')

    def __str__(self):
        return self.name

class GenderEnum(models.TextChoices):
    MAN = 'MAN', _('Man')
    WOMAN = 'WOMAN', _('Woman')


# Bảng Product
class Product(TimeStampedModel, StatusModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_id = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    url_handle = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    min_variant_price = models.DecimalField(max_digits=10, decimal_places=2)
    max_variant_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_sold = models.IntegerField(default=0)
    available_quantity = models.IntegerField(default=0)
    inventory_status = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=50, choices=GenderEnum.choices)
    product_type = models.CharField(max_length=50, null=True, blank=True)
    source_channel = models.ForeignKey(SourceChannel, on_delete=models.SET_NULL, null=True, blank=True, related_name='product_source_channel')

    def __str__(self):
        return self.name

# Bảng ProductSize
class ProductSize(TimeStampedModel, StatusModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    size_id = models.CharField(max_length=255, unique=True)
    size_name = models.CharField(max_length=50)
    position = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.size_name

# Bảng ProductColor
class ProductColor(TimeStampedModel, StatusModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    color_id = models.CharField(max_length=255, unique=True)
    color_name = models.CharField(max_length=50)
    url = models.URLField(max_length=255, null=True, blank=True)
    position = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.color_name

# Bảng Brand
class Brand(TimeStampedModel, StatusModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    brand_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    brand_name = models.CharField(max_length=255)

    def __str__(self):
        return self.brand_name

# Bảng ProductOption
class ProductOption(TimeStampedModel, StatusModel):
    option_name = models.CharField(max_length=255)

    def __str__(self):
        return self.option_name

# Bảng ProductAsset
class ProductAsset(TimeStampedModel, StatusModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_asset_id = models.CharField(max_length=255, unique=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_asset')
    asset_url = models.URLField(max_length=255)
    asset_type = models.CharField(max_length=50, choices=[('image', 'Image'), ('video', 'Video')])
    position = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.product.name} - {self.asset_type}"

# Bảng FactProductDetail
class FactProductDetail(TimeStampedModel, StatusModel): # Fact table for product options
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_option_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_detail')
    size = models.ForeignKey(ProductSize, on_delete=models.SET_NULL, null=True, blank=True, related_name='product_size')
    color = models.ForeignKey(ProductColor, on_delete=models.SET_NULL, null=True, blank=True, related_name='product_color')
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True, related_name='product_brand')
    option = models.ForeignKey(ProductOption, on_delete=models.SET_NULL, null=True, blank=True, related_name='product_option')
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Detail for {self.product.name}"


class CoreProduct(models.Model):
    product_data = models.JSONField()

    class Meta:
        db_table = 'core_coreproduct'  # Tên bảng trong PostgreSQL
        verbose_name = 'Core Product'
        verbose_name_plural = 'Core Products'