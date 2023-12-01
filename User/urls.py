from django.urls import path
from .views import (
                    UserCreateView, UserRetrieveView, 
                    UserLoginView, UserLogoutView, 
                    UserListView, TokenRefreshView,
                    UserUpdateView, DeactivateAccountView,
                    )

urlpatterns = [
    #path('list', UserListView.as_view(), name='user-list'),
    path('create', UserCreateView.as_view(), name='user-create'),
    path('own_info', UserRetrieveView.as_view(), name='user-detail'),
    path('update_own_info', UserUpdateView.as_view(), name='user-update'),
    path('deactivate_account', DeactivateAccountView.as_view(), name='deactivate-account'),
    path('login', UserLoginView.as_view(), name='user-login'),
    path('logout', UserLogoutView.as_view(), name='user-logout'),
    path('token/refresh', TokenRefreshView.as_view(), name='token-refresh'),
]
