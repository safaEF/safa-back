from django.urls import path

from .views import  ( 
    register, login, logout, AuthenticatedUser, PermissionAPIView, RoleViewSet, UserGenericAPIView,
    ProfileInfoAPIView, ProfilePasswordAPIView
)

urlpatterns = [
    path('register', register),
    path('login', login),
    path('logout', logout),
    path('user', AuthenticatedUser.as_view()),
    path('permissions', PermissionAPIView.as_view()),
    path('roles', RoleViewSet.as_view()),
    path('roles/create', RoleViewSet.as_view()),
    path('roles/<str:pk>', RoleViewSet.as_view()),
    path('users/info', ProfileInfoAPIView.as_view()),
    path('users/password', ProfilePasswordAPIView.as_view()),
    # path('users', UserGenericAPIView.as_view()),
    path('users/<str:pk>', UserGenericAPIView.as_view(),{'pk':'pk'}),
]