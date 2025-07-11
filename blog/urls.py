from django.urls import path
from . import views
from . import apis
urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/new/', views.post_create, name='post_create'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('post/<slug:slug>/edit/', views.post_edit, name='post_edit'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('contact/', views.contact_view, name='contact'),

    path("api/word-lists/", apis.word_lists_api, name="word_lists_api"),
]
