from django.urls import path
from .views import UserCreateView, UserRetrieveUpdateDestroyView, UserLoginView, UserLogoutView, UserListView, TokenRefreshView

urlpatterns = [
    path('list/', UserListView.as_view(), name='user-list'),
    path('create/', UserCreateView.as_view(), name='user-create'),
    path('own_info/<int:pk>/', UserRetrieveUpdateDestroyView.as_view(), name='user-detail'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('logout/', UserLogoutView.as_view(), name='user-logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]
