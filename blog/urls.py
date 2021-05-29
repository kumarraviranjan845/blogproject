from django.urls import path
from . import views
from .views import (
    PostListView, 
    PostDetailView, 
    PostCreateView, 
    PostUpdateView, 
    PostDeleteView, 
    UserPostListView, 
    UserLikeView,
)

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>/', UserPostListView.as_view(), name='user-blogs'),
    path('blog/new/', PostCreateView.as_view(), name='blog-create'),
    path('blog/<int:pk>/', PostDetailView.as_view(), name='blog-detail'),
    path('blog/<int:pk>/update/', PostUpdateView.as_view(), name='blog-update'),
    path('blog/<int:pk>/delete/', PostDeleteView.as_view(), name='blog-delete'),
    path('like/<int:pk>', views.like_view, name='like-post'),
    path('likes/<str:username>', UserLikeView.as_view(), name='user-likes'),
    path('search/', views.search_result, name='search'),
    path('about/', views.about, name='blog-about')
]
