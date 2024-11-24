from app.crawler import etl
from app.core.models.base import Category, Product


class TransformYodyCategory(etl.Transform):
    def execute(self, raw_data: list[dict]) -> list[Category]:
        category_name = raw_data.get("category")
        if not category_name:  # If category is None or empty
            print(f"Skipping invalid data: {raw_data}")  # Log and skip
            return []
        
        category, _ = Category.objects.update_or_create(
            category_id=str(raw_data["category_id"]),
            defaults={"name": raw_data["category"]},
        )

        print(f"Transformed {category}")
        return [category]
    

class TransformYodyProduct(etl.Transform):
    def execute(self, raw_data: list[dict]) -> list[Product]:
        product_name = raw_data.get("name")
        if not product_name:  
            print(f"Skipping invalid data: {raw_data}")  
            return []

        category_id = raw_data.get("category_id")
        if not category_id:  
            print(f"Skipping invalid data: {raw_data}")  
            return []

        category = Category.objects.filter(category_id=str(category_id)).first()
        if not category:  
            print(f"Category not found for product: {raw_data}")  
            return []

        product, _ = Product.objects.update_or_create(
            product_id=str(raw_data["product_id"]),
            defaults={
                "name": product_name,
                "price": raw_data.get("price"),
                "category": category,
            },
        )

        print(f"Transformed {product}")
        return [product]