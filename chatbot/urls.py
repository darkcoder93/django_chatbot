from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_interface, name='chat_interface'),
    path('test/', views.test_chat_api, name='test_chat_api'),
    path('api/chat/', views.chat_api, name='chat_api'),
    path('api/chat/history/<str:session_id>/', views.get_chat_history, name='chat_history'),
    path('api/chat/results/<str:session_id>/', views.get_query_results, name='query_results'),
    path('api/download/', views.download_data, name='download_data'),
    path('api/health/', views.health_check, name='health_check'),
    path('api/test/', views.test_chat_api, name='test_chat_api'),
] 