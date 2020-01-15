from django.urls import path
from apps.core.api import views as api_views

urlpatterns = [
    path('create_message', api_views.create_message, name='create-message'),
    path(
        'get_message/<int:message_id>/<str:access_token>/',
        api_views.get_message,
        name='get-message',
    ),
    path(
        'get_last_active_app_config/',
        api_views.get_last_active_app_config,
        name='get-last-active-app-config'
    ),
]