from django.urls import path
from .views import ListCreatePost,SinglePost,RegisterView,MyTokenObtainPairView,getPostUpvote
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)



urlpatterns = [
 path('',ListCreatePost.as_view(),name='list_create_post'),
 path('post/<pk>',SinglePost.as_view(),name='single_post'),
 path('post/<pk>/upvote',getPostUpvote.as_view(),name='single_post'),
 path('register/',RegisterView.as_view(),name='register'),
 path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
 path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

 
]
