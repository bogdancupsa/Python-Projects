
from django.urls import path
from .views import CustomAuthToken, CustomUserListCreateView, CustomUserRetrieveUpdateDestroyView

urlpatterns = [
    path('api-token-auth/', CustomAuthToken.as_view(), name='api_token_auth'),
    path('clients/', CustomUserListCreateView.as_view(), name = 'client-list-create'),
    path('clients/<int:pk>/', CustomUserRetrieveUpdateDestroyView.as_view(), name = 'client-retrieve-update-destroy'),
]
