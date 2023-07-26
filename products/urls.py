from django.urls import path
from .views import *

urlpatterns = [
    path('api/products/', ProductListAPIView.as_view(), name='product-list'),
    path('api/products/create/', ProductCreateView.as_view(), name='product-create'),
    path('api/products/<int:product_id>/', ProductDetailView.as_view(), name='product-detail'),
    path('api/geners/', GenereListView.as_view(), name='genere-list'),
    # path('products/update/<int:pk>/', ProductUpdateView.as_view(), name='product-update'),
    # path('products/delete/<int:pk>/', ProductDeleteView.as_view(), name='product-delete'),

    ####################################### ADMIN API ####################################################
    path('api/admin/products/', ProductListAdmin.as_view(), name='admin-product-list'),
    path('api/admin/product/status/', ApproveProductAPI.as_view(), name='admin-pt'),

]