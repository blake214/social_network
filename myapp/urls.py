from django.urls import path
from . import views
from . import api

urlpatterns = [
    path('', views.UserDashboard, name='index'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.Logout, name='logout'),
    path('update_user/', views.UserUpdate.as_view(), name='update_user'),
    path('user_view/', views.UserView.as_view(), name='user_view'),
    path('thread/', views.ThreadView.as_view(), name='thread'),
    
    path('api/user/', api.UserPoint.as_view(), name='user_api'),
    path('api/user_search/', api.UserSearchPoint.as_view(), name='user_search_api'),
    path('api/user_gallery/', api.UserGalleryPoint.as_view(), name='user_gallery_api'),
    path('api/user_status/', api.UserStatusPoint.as_view(), name='user_status_api'),
    path('api/user_connection_junction/', api.UserConnectionJunctionPoint.as_view(), name='user_connection_junction_api'),
    path('api/user_connection_junctions_approved/', api.UserConnectionJunctionsPoint_ApprovedRecords.as_view(), name='user_connection_junctions_approved_api'),
    path('api/user_connection_junctions_pending/', api.UserConnectionJunctionsPoint_PendingRecords.as_view(), name='user_connection_junctions_pending_api'),
    path('api/user_connection_junctions_user/', api.UserConnectionJunctionsPoint_UserRecords.as_view(), name='user_connection_junctions_user_api'),
    # path('api/user_connection_junctions_connection/', api.UserConnectionJunctionsPoint_ConnectionRecords.as_view(), name='user_connection_junctions_connection_api'),
    path('api/thread/', api.ThreadPoint.as_view(), name='thread_api'),
    path('api/threads/', api.ThreadsPoint.as_view(), name='threads_api'),    
    path('api/user_thread_junction/', api.UserThreadJunctionPoint.as_view(), name='user_thread_junction_api'),
    path('api/user_thread_junctions/', api.UserThreadJunctionsPoint.as_view(), name='user_thread_junctions_api'),
    path('api/thread_messages/', api.ThreadMessagesPoint.as_view(), name='thread_messages_api'),
]