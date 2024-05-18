from django.shortcuts import render
from authentication.serializer import RegisterSerializer
from rest_framework import response, status, generics
from .models import User

class RegisterAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    
    def post(self,request):
        serializers = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
