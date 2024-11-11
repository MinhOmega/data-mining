from django.db import models

# Bảng Category
class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

# Bảng SourceChannel
class SourceChannel(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

# Bảng Product
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    source_channel = models.ForeignKey(SourceChannel, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

# Bảng ProductSize
class ProductSize(models.Model):
    size_name = models.CharField(max_length=50)

    def __str__(self):
        return self.size_name

# Bảng ProductColor
class ProductColor(models.Model):
    color_name = models.CharField(max_length=50)

    def __str__(self):
        return self.color_name

# Bảng Brand
class Brand(models.Model):
    brand_name = models.CharField(max_length=255)

    def __str__(self):
        return self.brand_name

# Bảng ProductOption
class ProductOption(models.Model):
    option_name = models.CharField(max_length=255)

    def __str__(self):
        return self.option_name

# Bảng ProductAsset
class ProductAsset(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    asset_url = models.URLField(max_length=255)
    asset_type = models.CharField(max_length=50, choices=[('image', 'Image'), ('video', 'Video')])

    def __str__(self):
        return f"{self.product.name} - {self.asset_type}"

# Bảng FactProductDetail
class FactProductDetail(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(ProductSize, on_delete=models.SET_NULL, null=True, blank=True)
    color = models.ForeignKey(ProductColor, on_delete=models.SET_NULL, null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    option = models.ForeignKey(ProductOption, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Detail for {self.product.name}"
