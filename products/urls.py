from django.urls import path
from .views import ProductListAPIView, ProductCreateView

urlpatterns = [
    path('api/products/', ProductListAPIView.as_view(), name='product-list'),
    path('api/products/create/', ProductCreateView.as_view(), name='product-create'),
    # path('products/update/<int:pk>/', ProductUpdateView.as_view(), name='product-update'),
    # path('products/delete/<int:pk>/', ProductDeleteView.as_view(), name='product-delete'),

]