from django.urls import path
from .views import upload_file, search_product

urlpatterns = [
    path('', upload_file, name='upload_file'),
    path('search-product/', search_product, name='search_product'),
]