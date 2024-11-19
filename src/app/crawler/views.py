from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from app.crawler.serializer import ProductLoadRequestSerializer

from app.crawler.partners.yody.extract import ExtractYodyCategory
from app.crawler.partners.yody.transform import TransformYodyCategory
from app.crawler.partners.yody.load import LoadCategoryData
from app.crawler.tasks.yody_category_crawler import YodyCategoryCrawler
from app.crawler.tasks.extract_yody_to_datalake import YodyProductCrawler
from app.crawler.tasks.load_data_to_postgres import LoadProductData

from app.core.models import Product, Category, Brand, FactProductDetail
import requests

# ETL process for Yody categories to Postgres
class YodyCategoryETLView(APIView):
    def post(self, request):
        # Extract parameters from the API request if needed
        status_param = request.data.get("status", "active")  # Default to 'active'

        # Initialize ETL components
        extract = ExtractYodyCategory(status=status_param)
        transform = TransformYodyCategory()
        load = LoadCategoryData()

        # Run the ETL process
        try:
            crawler = YodyCategoryCrawler()
            categories = crawler.run_etl(extract, transform, load)

            # Return success response with details
            return Response(
                {
                    "message": "ETL process completed successfully.",
                    "total_categories_processed": len(categories),
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            # Handle exceptions and return error response
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# Extract Yody products and save to MinIO
class YodyProductExtractView(APIView):
    def post(self, request):
        status_param = request.data.get("status", "active")

        try:
            # Run the extraction process
            crawler = YodyProductCrawler()
            crawler.run_extract(status=status_param)
            return Response({"message": "Product extraction initiated successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

# Load Yody products from MinIO to Postgres
class YodyProductLoadView(APIView):
    def post(self, request):
        serializer = ProductLoadRequestSerializer(data=request.data)
        print(f"Request data: {request.data}")
        if serializer.is_valid():
            bucket_name = serializer.validated_data["bucket_name"]
            object_name = serializer.validated_data["object_name"]

            print(f"Loading data from MinIO bucket: {bucket_name}, object: {object_name}")

            try:
                # Load data from MinIO to Postgres
                loader = LoadProductData(bucket_name, object_name)
                data = loader.execute()

                # Perform data loading to Postgres
                for item in data:
                    # print(item)
                    # Insert or update Category
                    try:
                        category, _ = Category.objects.update_or_create(
                            category_id=item["category_id"],
                            defaults={
                                "name": item["category"],
                                "description": item["category"],
                            }
                        )
                    except Exception as e:
                        print(f"Error inserting Category: {str(e)}")

                    # Insert or update Brand
                    try:
                        brand, _ = Brand.objects.update_or_create(
                            brand_id=item["brand_id"],
                            defaults={
                                "brand_name": item["brand"],
                            }
                        )
                    except Exception as e:
                        print(f"Error inserting Brand: {str(e)}")

                return Response({"message": "Product data loaded to Postgres successfully."}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
# Trigger the Yody consumer DAG in Airflow
class TriggerYodyConsumerView(APIView):
    def post(self, request):
        # URL to trigger the Airflow DAG
        airflow_url = "http://localhost:8081/api/v1/dags/yody_consumer_dag/dagRuns"

        try:
            response = requests.post(
                airflow_url,
                json={"conf": {}},  # Optional: Pass DAG run configuration
                auth=("airflow", "airflow"),  # Replace with your Airflow username and password
            )
            if response.status_code == 200:
                return Response(
                    {"message": "Yody consumer DAG triggered successfully."},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": response.json()},
                    status=response.status_code,
                )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)