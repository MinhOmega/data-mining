from app.crawler import etl
from app.core.models.base import Category


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