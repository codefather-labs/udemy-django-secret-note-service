from rest_framework import status
from rest_framework.response import Response


class Request:
    @staticmethod
    def post(func):
        def wrapper(request, *args, **kwargs):
            if request.method == 'POST':
                return func(request, *args, **kwargs)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

        return wrapper

    @staticmethod
    def get(func):
        def wrapper(request, message_id, access_token, *args, **kwargs):
            if request.method == 'GET':
                return func(request, message_id, access_token, *args, **kwargs)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

        return wrapper
