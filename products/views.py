from django.shortcuts import render
from rest_framework import generics, status, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Product, Genere, Review, SavedMovies
from .serializers import *
from users.cloudinary_utils import upload_files
from django.http import QueryDict
from .pagination import FilterPagination
from django_filters.rest_framework import DjangoFilterBackend
from users.permessions import IsAdmin, IsSuperAdmin


class ProductListAPIView(generics.ListAPIView):
    # queryset = Product.objects.filter(is_active=True).order_by('-created_at')
    queryset = Product.custom_objects.get_is_active()
    permission_classes = (AllowAny,)
    serializer_class = ProductRetriveSerializer
    pagination_class = FilterPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['genere']
    search_fields = ['title', 'description']


class ProductDetailView(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)
    queryset = Product.objects.all()
    serializer_class = ProductRetriveSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'product_id'


class ProductCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = ProductCreateSerializer

    def post(self, request, *args, **kwargs):
        data = QueryDict('', mutable=True)
        data.update(request.data)
        data['customer'] = request.user.id
        data['image'] = ""
        data['video'] = ""
        data['genere'] = 1
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            image = request.FILES['image']
            video = request.FILES['video']
            title = request.data["title"]
            image_url = f'weedoc/videos/{title.replace(" ", "_")}/image'
            video_url = f'weedoc/videos/{title.replace(" ", "_")}/video'
            resulted_image_url = upload_files(image, image_url, 'image')
            resulted_video_url = upload_files(video, video_url, 'video')
            data['image'] = resulted_image_url
            data['video'] = resulted_video_url[0]
            data['duration'] = resulted_video_url[1]
            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                geners = Genere.objects.filter(id__in=list(eval(request.data['genere'])))
                product =  serializer.save()
                product.genere.set(geners)
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
        data = QueryDict('', mutable=True)
        data.update(request.data)
        data['cast_member'] = request.data['user']
        data['role'] = request.data['role']
        data['product'] = self.kwargs['movie_id']
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            casts = CastMember.objects.filter(product=self.kwargs['movie_id']).order_by('-id')
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
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        product.likes.add(user)
        product.dislikes.remove(user)

        serializer = ProductRetriveSerializer(product, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class DislikeProductView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id):
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        product.dislikes.add(user)
        product.likes.remove(user)

        serializer = ProductRetriveSerializer(product, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class ReviewList(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = (AllowAny,)
    
    def get_queryset(self):
        movie_id = self.kwargs['movie_id']  # Assuming 'movie_id' is passed as a URL parameter
        queryset = Review.objects.filter(movie_id=movie_id)
        return queryset
    

class AddReviewView(generics.CreateAPIView):
    serializer_class = ReviewAddSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        data = QueryDict('', mutable=True)
        data.update(request.data)
        data['user'] = request.user.id
        data['movie'] = self.kwargs['movie_id']
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SavedVideosView(APIView):
    serializer_class = SavedMoviesSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        data = QueryDict('', mutable=True)
        data.update(request.data)
        data['user'] = request.user.id
        data['movie'] = self.kwargs['movie']
        saved_movie = SavedMovies.objects.filter(user=data['user'], movie=data['movie'])
        if saved_movie.count() > 0:
            saved_movie.delete()
            return Response({'sucess': 'movie removed sucessfully'}, status=status.HTTP_200_OK)
        else:
            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({'sucess': 'movie saved sucessfully'}, status=status.HTTP_200_OK)
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
    
    def get_queryset(self):
        user = self.request.user
        return Review.objects.filter(user=user)


##################################################### ADMIN API ###############################################################


class ProductListAdmin(generics.ListAPIView):
    queryset = Product.custom_objects.order_by('-id')
    permission_classes = (IsAdmin, )
    serializer_class = ProductRetriveSerializer
    pagination_class = FilterPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['genere']
    search_fields = ['status']


class ApproveProductAPI(generics.UpdateAPIView):
    queryset = Product.custom_objects.order_by('-id')
    permission_classes = (IsAdmin, )
    serializer_class = ProductCreateSerializer

    def put(self, request, *args, **kwargs):
        product = Product.objects.filter(id=request.data['id'])
        data = QueryDict('', mutable=True)
        data.update(request.data)
        serializer = self.serializer_class(product, partial=True, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)