from django.urls import include, path


urlpatterns = [
    path('', include('app.crawler.urls')),
    path('', include('app.core.urls')),
]