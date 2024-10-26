import os
from django.shortcuts import render
from rest_framework import generics, status, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import PrefferedLanguages, Product, Genere, Review, SavedMovies, ViewsCount
from .serializers import *
from users.cloudinary_utils import upload_files
from django.http import QueryDict
from .pagination import FilterPagination, ProductsPagination
from django_filters.rest_framework import DjangoFilterBackend
from users.permessions import IsAdmin, IsSuperAdmin
from products.notification import add_notification
from config.storage_backends import MediaDelete, MediaStorage


class ProductListAPIView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    pagination_class = ProductsPagination
    serializer_class = ProductRetriveSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["genere"]
    search_fields = ["title", "description"]

    def get_queryset(self):
        try:
            user = self.request.user
            if user.is_authenticated:
                lang = list(
                    PrefferedLanguages.objects.filter(user=user).values_list(
                        "language_id", flat=True
                    )
                )
                prod = Product.objects.filter(
                    languages__in=lang, status="approved"
                ).order_by("-created_at")
                rem = (
                    Product.objects.filter(status="approved")
                    .exclude(languages__in=lang)
                    .order_by("-created_at")
                )
                if not self.request.GET.get("search", None):
                    combined = prod.union(rem)
                    return combined
                else:
                    return Product.custom_objects.get_is_active()
            else:
                queryset = Product.objects.filter(status="approved").order_by("?")
                return queryset
        except:
            return Product.custom_objects.get_is_active()


class BannerProductList(APIView):

    def get(self, request, *args, **kwargs):
        # user = request.user
        # if user.is_authenticated:
        #     lang = list(
        #         PrefferedLanguages.objects.filter(user=user).values_list(
        #             "language_id", flat=True
        #         )
        #     )
        #     prod = Product.objects.filter(
        #         languages__in=lang, status="approved"
        #     ).order_by("-created_at")

        #     if prod.count() >= 5:
        #         combined = prod[:5]
        #     else:
        #         rem = (
        #             Product.objects.filter(status="approved")
        #             .exclude(languages__in=lang)
        #             .order_by("-created_at")
        #         )
        #         combined = prod.union(rem)[:5]
        # else:
        combined = Product.objects.filter(status="approved").order_by("-created_at")[:5]
        response = ProductRetriveSerializer(combined, many=True, context={"request": request}).data
        return Response(response)



class ProductDetailView(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)
    queryset = Product.objects.all()
    serializer_class = ProductRetriveSerializer
    lookup_field = "id"
    lookup_url_kwarg = "product_id"


from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser


class ProductCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductCreateSerializer

    def post(self, request, *args, **kwargs):
        parser_classes = (MultiPartParser, FormParser, FileUploadParser)
        if "genere" not in request.data.keys():
            return Response({"genere": ["This field is required"]})
        if request.data["genere"] == "":
            return Response({"genere": ["Genere is empty"]})
        data = QueryDict("", mutable=True)
        data.update(request.data)
        data["customer"] = request.user.id
        data["image"] = ""
        data["video"] = ""
        data["genere"] = 1
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            image = request.FILES["image"]
            video = request.FILES["video"]
            title = request.data["title"]
            image_url = f'weedoc/videos/{title.replace(" ", "_")}/image'
            video_url = f'weedoc/videos/{title.replace(" ", "_")}/video'
            video_file = request.FILES["video"]
            # video_chunks = [chunk for chunk in video_file.chunks()]
            resulted_image_url = upload_files(image, image_url, "image")
            resulted_video_url = upload_files(video_file, video_url, "video")
            data["image"] = resulted_image_url
            data["video"] = resulted_video_url[0]
            data["duration"] = resulted_video_url[1]
            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                geners = Genere.objects.filter(
                    id__in=list(eval(request.data["genere"]))
                )
                product = serializer.save()
                product.genere.set(geners)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductUploadView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductCreateSerializer

    def post(self, request, *args, **kwargs):
        parser_classes = (MultiPartParser, FormParser, FileUploadParser)
        if "genere" not in request.data.keys():
            return Response({"genere": ["This field is required"]})
        if request.data["genere"] == "":
            return Response({"genere": ["Genere is empty"]})
        data = QueryDict("", mutable=True)
        data.update(request.data)
        data["customer"] = request.user.id
        data["image"] = ""
        data["video"] = ""
        data["genere"] = 1
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            image = request.FILES.get("image")
            video = request.FILES.get("video")
            title = request.data["title"]
            image_url = None
            video_url = None
            if image:
                file_directory_within_bucket = f"{title.replace(' ', '_')}/image/"
                file_path_within_bucket = os.path.join(
                    file_directory_within_bucket, image.name.replace(" ", "_")
                )
                media_storage = MediaStorage()
                image_url = media_storage.url(file_path_within_bucket).split("?", 1)
                media_storage.save(file_path_within_bucket, image)
            if video:
                file_location_within_bucket = f"{title.replace(' ', '_')}/video/"
                file_location = os.path.join(
                    file_location_within_bucket, video.name.replace(" ", "_")
                )
                video_storage = MediaStorage()
                video_url = video_storage.url(file_location).split("?", 1)
                video_storage.save(file_location, video)
            data["image"] = image_url[0] if image_url else ""
            data["video"] = video_url[0] if video_url else ""
            data["duration"] = None
            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                geners = Genere.objects.filter(
                    id__in=list(eval(request.data["genere"]))
                )
                product = serializer.save()
                product.genere.set(geners)
                msg = f"{product.title} is under review."
                notification = add_notification(product.customer, msg)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddCastView(generics.CreateAPIView):
    serializer_class = CastSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        # if CastMember.objects.filter(cast_member=request.data['user']).exists():
        #     return Response({'error': 'cast exists'}, status=status.HTTP_200_OK)
        data = QueryDict("", mutable=True)
        data.update(request.data)
        data["cast_member"] = request.data["user"]
        data["role"] = request.data["role"]
        data["product"] = self.kwargs["movie_id"]
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            casts = CastMember.objects.filter(product=self.kwargs["movie_id"]).order_by(
                "-id"
            )
            res = CastRetriveSerializer(casts, many=True)
            return Response(res.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GenereListView(generics.ListAPIView):
    queryset = Genere.objects.all()
    serializer_class = GenereRetriveSerializer
    permission_classes = (AllowAny,)


class LikeProductView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id):
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND
            )

        user = request.user
        if product.likes.filter(id=user.id).exists():
            product.likes.remove(user)
        else:
            product.likes.add(user)
        product.dislikes.remove(user)

        serializer = ProductRetriveSerializer(product, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class DislikeProductView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id):
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND
            )

        user = request.user
        if product.dislikes.filter(id=user.id).exists():
            product.dislikes.remove(user)
        else:
            product.dislikes.add(user)
        product.likes.remove(user)

        serializer = ProductRetriveSerializer(product, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewList(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        movie_id = self.kwargs[
            "movie_id"
        ]  # Assuming 'movie_id' is passed as a URL parameter
        queryset = Review.objects.filter(movie_id=movie_id)
        return queryset


class AddReviewView(generics.CreateAPIView):
    serializer_class = ReviewAddSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        data = QueryDict("", mutable=True)
        data.update(request.data)
        data["user"] = request.user.id
        data["movie"] = self.kwargs["movie_id"]
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SavedVideosView(APIView):
    serializer_class = SavedMoviesSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        data = QueryDict("", mutable=True)
        data.update(request.data)
        data["user"] = request.user.id
        data["movie"] = self.kwargs["movie"]
        saved_movie = SavedMovies.objects.filter(user=data["user"], movie=data["movie"])
        if saved_movie.count() > 0:
            saved_movie.delete()
            return Response(
                {"sucess": "movie removed sucessfully"}, status=status.HTTP_200_OK
            )
        else:
            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"sucess": "movie saved sucessfully"}, status=status.HTTP_200_OK
                )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListSavedMovies(generics.ListAPIView):
    serializer_class = SavedMovieListsSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = SavedMovies.objects.filter(user=self.request.user)
        return queryset


class ListReviewsGiven(generics.ListAPIView):
    serializer_class = ListAllReviewsGivenSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["movie"]
    search_fields = ["movie__title"]

    def get_queryset(self):
        user = self.request.user
        return Review.objects.filter(user=user).order_by("-id")


class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationAddSerializer
    permission_classes = (IsAuthenticated,)
    # filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    # filterset_fields = ['movie']
    # search_fields = ['movie__title']

    def get_queryset(self):
        user = self.request.user
        return Notification.objects.filter(recipient=user).order_by("-id")


import json


class NotificationStatusUpdate(APIView):
    serializer_class = NotificationAddSerializer
    permission_classes = (IsAuthenticated,)

    def update_notification(self, model, data):
        serializer = self.serializer_class(model, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer

    def put(self, request, *args, **kwargs):
        notification_ids = request.data["id"]

        if isinstance(notification_ids, int):
            notification_ids = [notification_ids]

        notifications = Notification.objects.filter(id__in=notification_ids)
        if not notifications.exists():
            return Response(
                {"error": "Notifications not found"}, status=status.HTTP_404_NOT_FOUND
            )

        updated_notifications = []
        for notification in notifications:
            try:
                updated_notification = self.update_notification(
                    notification, request.data
                )
                updated_notifications.append(updated_notification.data)
            except serializers.ValidationError as e:
                return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {"success": "Data Updated", "updated_notifications": updated_notifications}
        )


from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from .models import Product, Notification, User  # Assuming these models are imported

class ExtractMovieData(APIView):
    permission_classes = [IsAuthenticated]

    def extract_title(self, content: str):
        """
        Extracts the title from the shared content and returns the product ID if found.
        """
        try:
            title = content.replace(" has shared ", "--_--").replace(" for you to watch.", "").split("--_--")[-1]
            product = Product.objects.filter(title=title).first()
            
            if not product:
                raise ObjectDoesNotExist(f"Product with title '{title}' does not exist.")

            return product.id

        except ObjectDoesNotExist as e:
            raise e
        except Exception as e:
            raise ValueError("Error extracting title from the message.") from e

    def post(self, request, *args, **kwargs):
        """
        Receives content and returns the product ID.
        """
        try:
            message = request.data.get("content")
            if not message:
                return Response({"detail": "Content is required."}, status=status.HTTP_400_BAD_REQUEST)

            prod_id = self.extract_title(message)
            return Response({"product_id": prod_id}, status=status.HTTP_200_OK)

        except ObjectDoesNotExist as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": "An error occurred while processing the request."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ShareMovies(APIView):
    permission_classes = [IsAuthenticated]

    def generate_notification_msg(self, user_name, title):
        """
        Generates the notification message.
        """
        return f"{user_name} has shared {title} for you to watch."

    def post(self, request, *args, **kwargs):
        """
        Sends a notification to a user with the movie details.
        """
        try:
            product_id = request.data.get("prod_id")
            to_user_id = request.data.get("user_id")
            
            if not product_id or not to_user_id:
                return Response({"detail": "Product ID and User ID are required."}, status=status.HTTP_400_BAD_REQUEST)
            product = Product.objects.get(id=product_id)
            to_user = User.objects.get(id=to_user_id)
            title = product.title
            user_name = request.user.get_full_name()
            content = self.generate_notification_msg(user_name, title)
            Notification.objects.create(recipient=to_user, content=content)

            return Response({"detail": "Notification Sent to Follower!"}, status=status.HTTP_200_OK)

        except Product.DoesNotExist:
            return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({"detail": "Recipient user not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": "Failed to share the movie."}, status=status.HTTP_400_BAD_REQUEST)



class UserFollowersAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        try:
            user:User = request.user
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        followers = user.followers.all()
        serializer = FollowerSerializer(followers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



##################################################### ADMIN API ###############################################################


class ProductListAdmin(generics.ListAPIView):
    queryset = Product.custom_objects.order_by("-id")
    permission_classes = (IsAdmin,)
    serializer_class = ProductRetriveSerializer
    # pagination_class = FilterPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["genere"]
    search_fields = ["status"]


class ApproveProductAPI(generics.UpdateAPIView):
    queryset = Product.custom_objects.order_by("-id")
    permission_classes = (IsAdmin,)
    serializer_class = ProductCreateSerializer

    def put(self, request, *args, **kwargs):
        try:
            product = Product.objects.get(id=request.data["id"])
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND
            )
        data = QueryDict("", mutable=True)
        data.update(request.data)
        serializer = self.serializer_class(product, partial=True, data=data)
        if serializer.is_valid():
            serializer.save()
            msg = f"{product.title} has been {request.data['status']}."
            notification = add_notification(product.customer, msg)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListLanguages(generics.ListAPIView):
    queryset = Languages.objects.order_by("name")
    serializer_class = LanguagesSerializer
    permission_classes = (AllowAny,)


class AdminLanguages(APIView):
    permission_classes = (IsAdmin,)

    def post(self, request, *args, **kwargs):
        data = request.data

        ser = LanguagesSerializer(data=data)
        if ser.is_valid():
            ser.save()
            return Response({"success": "New Language Created"})
        else:
            return Response(
                {"error": str(ser.errors)}, status=status.HTTP_400_BAD_REQUEST
            )


class UsersPrefferedLanguages(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        data = []
        check = PrefferedLanguages.objects.filter(user=request.user)
        if check.count() >= 3:
            return Response(
                {"error": "User Already Selected the Languages"},
                status=status.HTTP_302_FOUND,
            )
        languages = eval(str(request.data["languages"]))
        for each in languages:
            lang = PrefferedLanguages()
            lang.user = request.user
            lang.language_id = each
            data.append(lang)

        if len(data) <= 3:
            res = PrefferedLanguages.objects.bulk_create(data)
        else:
            return Response(
                {"error": "Select Upto three languages"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {"success": "Preffered Languages Updated Successfully"},
            status=status.HTTP_202_ACCEPTED,
        )


class DeleteProductData(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            product = Product.objects.get(id=request.data["id"])
        except:
            return Response(
                {"error": "Product DoesNotExist"}, status=status.HTTP_404_NOT_FOUND
            )
        if product.video:
            MediaDelete().s3_delete(product.video)
        if product.image:
            MediaDelete().s3_delete(product.image)
        product.delete()
        return Response(
            {"success": "Product Deleted Successfully"}, status=status.HTTP_200_OK
        )


class MostLikedProduct(APIView):

    def get(self, request, *args, **kwargs):
        product = Product.custom_objects.get_is_active().order_by("-likes")[:15]
        return Response(product.values("title", "likes"), status=status.HTTP_200_OK)


class ProductViews(APIView):

    def post(self,request,  *args, **kwargs):
        count = request.data.get("count")
        product_id = request.data.get("product_id")
        try:
            obj = ViewsCount.objects.get(product_id=product_id)
            obj.count += count
            obj.save()
        except ViewsCount.DoesNotExist:
            try:
                obj = ViewsCount.objects.create(**request.data)
            except Exception as e:
                return Response({"error": str(e)})
        return Response({"views":obj.count})