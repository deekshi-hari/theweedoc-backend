from django.urls import path
from .views import *

urlpatterns = [
    path("api/products/", ProductListAPIView.as_view(), name="product-list"),
    path("api/products/create/", ProductCreateView.as_view(), name="product-create"),
    path("api/products/create/upload/", ProductUploadView.as_view()),
    path(
        "api/products/cast/add/<int:movie_id>/", AddCastView.as_view(), name="cast_add"
    ),
    path(
        "api/products/<int:product_id>/",
        ProductDetailView.as_view(),
        name="product-detail",
    ),
    path("api/geners/", GenereListView.as_view(), name="genere-list"),
    path(
        "api/product/<int:product_id>/like/",
        LikeProductView.as_view(),
        name="like_product",
    ),
    path(
        "api/product/<int:product_id>/dislike/",
        DislikeProductView.as_view(),
        name="dislike_product",
    ),
    path("api/reviews/<int:movie_id>/", ReviewList.as_view(), name="review_list"),
    path("api/reviews/add/<int:movie_id>/", AddReviewView.as_view(), name="review_add"),
    path("api/reviews/given/", ListReviewsGiven.as_view(), name="all_reviews_given"),
    path(
        "api/movies/list/saved/", ListSavedMovies.as_view(), name="movie_save_or_remove"
    ),
    path(
        "api/movies/save/<int:movie>/",
        SavedVideosView.as_view(),
        name="movie_save_or_remove",
    ),
    path(
        "api/notifications/", NotificationListView.as_view(), name="notification_list"
    ),
    ####################################### ADMIN API ####################################################
    path("api/admin/products/", ProductListAdmin.as_view(), name="admin-product-list"),
    path("api/admin/product/status/", ApproveProductAPI.as_view(), name="admin-pt"),
]
