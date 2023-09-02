from django.urls import include, path
from . import views
from . import api


urlpatterns = [
    #path('', views.GeneList.as_view(), name='index'),
    path('', views.index, name='index'),
    path('app/', views.SPA, name='spa'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('list_friends/', views.appFriendsList, name='list_friends'),    
    path('search_friends/', views.appUserList, name='search_friends'),    
    path('upload_media/', views.user_upload_media, name='upload_media'),
    path('status_update/', views.create_status_update, name='status_update'),
    path('api/image/', api.ImageDetail.as_view(), name="image_api"),
    path('api/images/', api.ImageList.as_view(), name="image_api"),
    path('<str:room_name>/', views.room, name='room'),
]
