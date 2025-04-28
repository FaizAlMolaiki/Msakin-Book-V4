from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.conversations_list, name='conversation_list'),
    path('<int:user_id>/', views.chat_room, name='chat_room'),
    path('api/conversations/', views.get_conversations, name='get_conversations'),
    path('api/messages/mark-read/<int:conversation_id>/', views.mark_messages_as_read, name='mark_messages_as_read'),
]
