from rest_framework import serializers
from apps.core.models import Message, AppConfig


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Message
        fields = (
            'id', 'text', 'access_token', 'is_viewed'
        )

class AppConfigSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AppConfig
        fields = (
            'id', 'session_name', 'api_id', 'api_hash', 'is_active',
            'is_bot', 'bot_token'
        )
