"""All the views related to Task model"""

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator

from Authentication.jwt_utils import get_user_from_request

from .models import Task
from Authentication.models import UserModel
from .serializer import TaskSerializer, TaskUpdateSerializer


@api_view(['GET', 'POST'])
def task_list(request):
    """Create a task or get the list of tasks with filters and pagination"""

    if request.method == 'GET':
        tasks = Task.objects.all()

        keyword = request.query_params.get('keyword', None)
        task_id = request.query_params.get('id', None)

        if keyword is not None:
            tasks = tasks.filter(name__icontains=keyword) | tasks.filter(description__icontains=keyword)
        if task_id is not None:
            tasks = tasks.filter(id=task_id)
        
        paginator = Paginator(tasks, request.query_params.get('page_size', 10)) # Default page size is 10
        page = paginator.get_page(request.query_params.get('page', 1)) # Default page is 1

        serializer = TaskSerializer(page, many=True)
        return Response({
            'message': 'Tasks fetched',
            'count': paginator.count,
            'page_size': paginator.per_page,
            'page': page.number,
            'data': serializer.data
        }, status=status.HTTP_200_OK)
    
    if request.method == 'POST':
        user = get_user_from_request(request)
        # if token not passed or not valid
        if not user:
            response_data = {
                "message": "Not authenticated",
            }
            return Response(response_data, status=status.HTTP_401_UNAUTHORIZED)
        
        # Only user can create a task
        if not user:
            response_data = {
                "message": "Not allowed",
            }
            return Response(response_data, status=status.HTTP_403_FORBIDDEN)
        
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'message':'Task created successfully',
                'data': serializer.data,
            }
            return Response(response, status=status.HTTP_201_CREATED)
        response = {
            'message':'Something went wrong',
            'error': serializer.errors,
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['GET', 'PUT', 'DELETE'])
def task_detail(request, id):
    """ Get task details, update a task or delete a task"""

    try:
        tasks = Task.objects.get(pk=id)
    except Task.DoesNotExist:
        response_data = {
            "message": "Task not found"
        }
        return Response(response_data, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TaskSerializer(task)
        response = {
            'message': 'task fetched',
            'data': serializer.data
        }
        return Response(response)
    
    elif request.method == 'PUT':
        user = get_user_from_request(request)
        # if token not passed or not valid
        if not user:
            response_data = {
                "message": "Not authenticated",
            }
            return Response(response_data, status=status.HTTP_401_UNAUTHORIZED)
        
        # Only user can update a course
        if not user:
            response_data = {
                "message": "Not allowed",
            }
            return Response(response_data, status=status.HTTP_403_FORBIDDEN)
        
        serializer = TaskUpdateSerializer(task, data = request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
            'message': "Task updated",
            'data': serializer.data
            }
            return Response(response_data)
        response = {
        'message':'Something went wrong',
        'error': serializer.errors,
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        user = get_user_from_request(request)
        # if token not passed or not valid
        if not user:
            response_data = {
                "message": "Not authenticated",
            }
            return Response(response_data, status=status.HTTP_401_UNAUTHORIZED)
        
        # Only user can delete a task
        if not user:
            response_data = {
                "message": "Not allowed",
            }
            return Response(response_data, status=status.HTTP_403_FORBIDDEN)
        task.delete()
        response_data = {
            "message": "Task deleted successfully"
        }
        return Response(response_data, status=status.HTTP_204_NO_CONTENT)
