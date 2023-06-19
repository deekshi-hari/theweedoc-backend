# from django.shortcuts import render
# from rest_framework import generics, status
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import AllowAny, IsAuthenticated
# from .models import Product
# from .serializers import ProductSerializer


# # Create your views here.
# class ProductListAPIView(generics.ListAPIView):
#     queryset = Product.objects.all()
#     permission_classes = (AllowAny,)
#     serializer_class = ProductSerializer


# class ProductCreateView(generics.CreateAPIView):
#     permission_classes = (IsAuthenticated, )
#     serializer_class = ProductSerializer

#     def post(self, request, *args, **kwargs):
#         request.data['customer'] = request.user.id
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# class ProductUpdateView(generics.UpdateAPIView):
#     permission_classes = (IsAuthenticated,)
#     serializer_class = ProductSerializer
#     queryset = Product.objects.all()

#     def update(self, request, *args, **kwargs):
#         product = self.get_object()
#         if product.customer.id != request.user.id:
#             return Response({'error': 'you dont have permession to update'}, status=status.HTTP_403_FORBIDDEN)
#         serializer = ProductSerializer(product, partial=True, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# class ProductDeleteView(generics.DestroyAPIView):
#     permission_classes = (IsAuthenticated,)
#     serializer_class = ProductSerializer
#     queryset = Product.objects.all()

#     def delete(self, request, *args, **kwargs):
#         product = self.get_object()
#         if product.customer.id != request.user.id:
#             return Response({'error': 'you dont have permession to delete'}, status=status.HTTP_403_FORBIDDEN)
#         return self.destroy(request, *args, **kwargs)