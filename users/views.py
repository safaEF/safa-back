from rest_framework import exceptions
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView, GenericAPIView, UpdateAPIView, CreateAPIView

from rest_framework.generics import DestroyAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.views import APIView
from testproject.pagination import CustomPagination
from .authentication import generate_access_token, JWTAuthentication
from .models import User, Permission, Role
from .serializers import UserSerializer, PermissionSerializer, RoleSerializer


@api_view(['POST'])
def register(request):
    data = request.data
    print(data)
    if data['password'] != data['password_confirm']:
        raise exceptions.APIException('Passwords do not match!')

    serializer = UserSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = User.objects.filter(email=email).first()

    if user is None:
        raise exceptions.AuthenticationFailed('User not found!')

    if not user.check_password(password):
        raise exceptions.AuthenticationFailed('Incorrect Password!')

    response = Response()

    token = generate_access_token(user)
    response.set_cookie(key='jwt', value=token, httponly=True, samesite='none', secure=True)
    response.data = {
        'jwt': token
    }

    return response


@api_view(['POST'])
def logout(_):
    response = Response()
    response.delete_cookie(key='jwt')
    response.data = {
        'message': 'Success'
    }
    return response


class AuthenticatedUser(APIView):
    '''return the current user along with it's permission'''
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = UserSerializer(request.user).data
        print(data)
        if data['role']:
            data['permissions'] = [p['name'] for p in data['role']['permissions']]
            return Response(
                data
            )


class PermissionAPIView(ListAPIView):
    queryset = Permission.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = PermissionSerializer


class Genericroleview(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = RoleSerializer
    queryset = Role.objects.all()


class Listroleview(Genericroleview, ListAPIView):
    pagination_class = CustomPagination
    login_url = '/login/'
    redirect_field_name = 'login'


class RoleViewSet(Genericroleview, RetrieveUpdateDestroyAPIView, CreateAPIView):
    permission_classes = [IsAuthenticated]
    permission_object = 'roles'
    lookup_field = "id"
    lookup_url_kwarg = "pk"


class UserGenericAPIView(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserlistAPI(UserGenericAPIView, ListAPIView):
    pagination_class = CustomPagination
    login_url = '/login/'
    redirect_field_name = 'login'


class UserAPIView(UserGenericAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, CreateAPIView):
    permission_classes = [IsAuthenticated]
    permission_object = 'users'
    lookup_field = "id"
    lookup_url_kwarg = 'pk'

    def perform_create(self, serializer):
        serializer.save(role_id=self.request.data.get('role_id'))

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        user = User.objects.get(id=instance.id)
        user.email = request.data.get('email')
        user.first_name = request.data.get('first_name')
        user.last_name = request.data.get('last_name')
        roles = Role.objects.get(id=request.data.get('role_id'))
        user.role = roles
        user.save()
        return Response(UserSerializer(user).data)


class ProfileInfoAPIView(UpdateAPIView):

    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user


class ProfilePasswordAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, pk=None):
        user = request.user
        if request.data['password'] != request.data['password_confirm']:
            raise exceptions.ValidationError('Passwords do not match')
        user.set_password(request.data['password'])
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data)
