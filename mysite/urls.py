from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index),
    path('createGroup/', views.createGroup),
    path('joinGroup/',views.joinGroup),
    path('joinGroupList/',views.joinGroupList),
    path('login/', auth_views.LoginView.as_view()),
    path('register/', views.register_view),
    path('logout/', views.logout_view),
    path('groupList/', views.groupList_view),
    path('groupListPage/', views.showGroups),
    path('requestPage/', views.request_page_view),
    path('request/<int:group_ID>/<int:groupAdmin_ID>/', views.request_view),
    path('acceptGroupRequest/<int:req_ID>/', views.acceptRequest_view),
    path('declineGroupRequest/<int:req_ID>/', views.declineRequest_view),
    path('showActivity/<int:group_ID>/', views.showActivity_view),
    path('addActivity/<int:group_ID>/', views.addActivity_view),
    path('deleteActivity/<int:activity_ID>/', views.deleteActivity_view),
    path('showSchedule/', views.schedule_view),
    path('chat/<str:room_name>/', views.chat_view),
]
