from app.crawler.partners.yody.request import YodyRequest


class YodyAPI:
    def __init__(self):
        self.request = YodyRequest()

    def call_products(self, page: int, status: str) -> dict:
        response = self.request.get(f"/storefront-product/api/product/public/product-by-filter.json?status={status}&page={page}")
        return response.json()
    

if __name__ == '__main__':
    api = YodyAPI()
    print(api.call_products(1, "active"))

