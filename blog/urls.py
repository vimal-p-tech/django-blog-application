from django.urls import path,include
from .views import *
from . import views
app_name = 'blog'
urlpatterns = [
    path('edit_form/<int:blog_id>',get_edit_form,name='edit_form'),
    path('dashboard',BlogDashBoard.as_view(),name='dashboard'),
    path('create',BlogCreateView.as_view(),name='blog_create'),
    path('list',BlogList.as_view(),name='blog_list'),
    path('detail/<str:encrypted_pk>/',BlogDetail.as_view(),name='blog_detail'),
    path('manage/',ManageBlog.as_view(),name='manage_blog'),
    path('delete/<int:pk>/',DeleteBlog.as_view(),name='blog_delete'),
    path('',BlogListView.as_view(),name='index_blogs'),
    path('add_comment/<int:post_id>/',add_comment,name='add_comment'),
]

