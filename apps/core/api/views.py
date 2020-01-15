from django.utils.datastructures import MultiValueDictKeyError

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.core.api.serializers import MessageSerializer, AppConfigSerializer
from apps.core.models import Message, AppConfig
from apps.core.api.utils import Request


@api_view(['GET'])
def get_last_active_app_config(request):
    if request.method == 'GET':
        try:
            config = AppConfig.objects.filter(is_active=True).last()
        except AppConfig.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)

        serializer = AppConfigSerializer(config)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@Request.post
def create_message(request):
    try:
        text = request.data['text']
    except MultiValueDictKeyError:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    new_message = Message.objects.create(text=text)
    serializer = MessageSerializer(new_message)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@Request.get
def get_message(request, message_id, access_token):
    try:
        message = Message.objects.get(id=message_id)
    except Message.DoesNotExist:
        return Response(status=status.HTTP_204_NO_CONTENT)

    if str(access_token) == str(message.access_token):
        text = message.text

        # auto deleting after message gonna viewed
        message.is_viewed = True
        message.save()

        return Response({"text": text}, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
