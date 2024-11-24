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


# Load Yody products from MinIO to PostgreSQL
class YodyProductLoadView(APIView):
    def post(self, request):
        status_param = request.data.get("status", "active")

        try:
            # Run the loading process
            loader = LoadProductData()
            loader.run_load(status=status_param)
            return Response({"message": "Product loading initiated successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

# Trigger Yody products from MinIO to Kafka
class DAGTriggerYodyProductView(APIView):
    def post(self, request):
        serializer = ProductLoadRequestSerializer(data=request.data)
        if serializer.is_valid():
            bucket_name = serializer.validated_data["bucket_name"]
            object_name = serializer.validated_data["object_name"]

            try:
                # Step 1: Trigger Airflow DAG
                airflow_url = "http://localhost:8088/api/v1/dags/minio_to_kafka_dynamic/dagRuns"
                response = requests.post(
                    airflow_url,
                    json={
                        "conf": {  # Pass MinIO params to the DAG
                            "bucket_name": bucket_name,
                            "object_name": object_name,
                        }
                    },
                    auth=("admin", "admin"),  # Airflow username and password
                    headers={"Content-Type": "application/json"},
                )

                # Step 2: Handle Airflow Response
                if response.status_code == 200:
                    return Response(
                        {"message": "DAG triggered successfully."},
                        status=status.HTTP_200_OK,
                    )
                elif response.status_code == 404:
                    return Response(
                        {"error": "Airflow DAG not found. Ensure DAG ID is correct and registered."},
                        status=status.HTTP_404_NOT_FOUND,
                    )
                else:
                    return Response(
                        {
                            "error": f"Failed to trigger Airflow DAG. Status: {response.status_code}",
                            "details": response.json(),
                        },
                        status=response.status_code,
                    )

            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)