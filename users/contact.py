from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework import status

class ContactUsForm(APIView):

    def post(self, request, *args, **kwargs):
        data = request.data.dict()

        serializer = ContactUsSerializer(data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

# class ContactUsList(APIView):

#     def get(self, request, *args, **kwargs):
