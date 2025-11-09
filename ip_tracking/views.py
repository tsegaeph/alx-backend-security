from django.contrib.auth import authenticate
from django.http import JsonResponse
from django_ratelimit.decorators import ratelimit
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# Define Swagger schema for request body
login_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'username': openapi.Schema(type=openapi.TYPE_STRING, description='User username'),
        'password': openapi.Schema(type=openapi.TYPE_STRING, description='User password'),
    },
    required=['username', 'password']
)


@swagger_auto_schema(
    method='post',
    request_body=login_request_body,
    responses={
        200: 'Login successful',
        400: 'Bad request (missing username or password)',
        401: 'Invalid credentials',
        429: 'Too many requests'
    },
)
@api_view(['POST'])
@permission_classes([AllowAny])
@ratelimit(key='ip', rate='10/m', method='POST', block=True)  # 10 per minute authenticated
@ratelimit(key='ip', rate='5/m', method='POST', block=True)   # 5 per minute anonymous
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return JsonResponse({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)

    if user is not None:
        return JsonResponse({'message': f'Welcome, {username}!'}, status=status.HTTP_200_OK)
    else:
        return JsonResponse({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
