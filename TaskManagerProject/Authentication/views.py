""" All the views related to user"""

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator
from django.contrib.auth.hashers import check_password, make_password

from .models import UserModel
from .serializer import UserModelSerializer, UserModelUpdateSerializer
from .jwt_utils import generate_token, get_user_from_request

@api_view(['POST'])
def user_login(request):
    """user login"""

    email = request.data.get('email', None)
    password = request.data.get('password', None)
    user = None
    if not password or not email:
        return Response({'Message': 'email and password are required to login'}, 
                        status= status.HTTP_400_BAD_REQUEST)
    try:
        user = UserModel.objects.get(email=email)
    except UserModel.DoesNotExist:
        pass
    if user and check_password(password, user.password) and user.is_active:
        token = generate_token(user)
        return Response({
            'message': 'Successfull login',
            'token': token,
        })
    if user and check_password(password, user.password) and not user.is_active:
        return Response({
            'Message': 'account deactivated',
        }, status=status.HTTP_401_UNAUTHORIZED)
    return Response({'Message': 'Wrong credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET', 'POST'])
def user_list(request):
    """Get the list of users or post a user"""
    
    # commented as of now so we can create our first admins
    """
    user = get_user_from_request(request)
    # if token not passed or not valid
    if not user:
        response_data = {
            "message": "Not authenticated",
        }
        return Response(response_data, status=status.HTTP_401_UNAUTHORIZED)
        
    # If not user, only users can get the list of users or create a user
    if not isinstance(user):
        response_data = {
            "message": "Not allowed",
        }
        return Response(response_data, status=status.HTTP_403_FORBIDDEN) 
    """


    if request.method == 'GET':
        user = get_user_from_request(request)
        # if token not passed or not valid
        if not user:
            response_data = {
                "message": "Not authenticated",
            }
            return Response(response_data, status=status.HTTP_401_UNAUTHORIZED)
        # If not user, only users can get the list of users or create a user
        if not isinstance(user):
            response_data = {
                "message": "Not allowed",
            }
            return Response(response_data, status=status.HTTP_403_FORBIDDEN)
        # The code above is to be removed after uncommenting the lines above 
        
        users = UserModel.objects.all()
        username = request.query_params.get('username')
        email = request.query_params.get('email')
        is_active = request.query_params.get('isActive')
        user_id = request.query_params.get('id')


        paginator = Paginator(users, request.query_params.get('page_size', 10)) # Default page size is 10
        page = paginator.get_page(request.query_params.get('page', 1)) # Default page is 1

        serializer = UserModelSerializer(page, many=True)
        return Response({
            'message': 'users fetched successfully',
            'count': paginator.count,
            'page_size': paginator.per_page,
            'page': page.number,
            'data': serializer.data
        }, status=status.HTTP_200_OK)
    
    if request.method == 'POST':
        serializer = UserModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'message': 'User created',
                'data': serializer.data,
            }
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, id):
    """ Get user  details, update a user and delete a user"""


    user = get_user_from_request(request)
    # if token not passed or not valid
    if not user:
        response_data = {
            "message": "Not authenticated",
        }
        return Response(response_data, status=status.HTTP_401_UNAUTHORIZED)
    
    # Only a user cant get, update or delete a user
    if not user:
        response_data = {
            "message": "Not allowed",
        }
        return Response(response_data, status=status.HTTP_403_FORBIDDEN)

    try:
        user = UserModel.objects.get(pk=id)
    except UserModel.DoesNotExist:
        response_data = {
            "message": "User not found"
        }
        return Response(response_data, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserModelSerializer(user)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        password = request.data.get('password')
        if password is not None:
            request.data['password'] = make_password(password)
        serializer = UserModelUpdateSerializer(user, data = request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
            'message': "User updated",
            'data': serializer.data
        }
            return Response(response_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        user.delete()
        response_data = {
            "message": "User deleted successfully"
        }
        return Response(response_data, status=status.HTTP_204_NO_CONTENT)
