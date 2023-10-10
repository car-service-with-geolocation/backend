from djoser.views import UserViewSet
from rest_framework.response import Response
from rest_framework import status

from .serializers import CustomUserSerializer


class CustomUserViewSet(UserViewSet):
    serializer = CustomUserSerializer

    def create(self, request, *args, **kwargs):
        registration_by_phone = request.data.get('phone_number', None)
        registration_by_email = request.data.get('email', None)

        if registration_by_phone:
            serializer = CustomUserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)

        if registration_by_email:
            return super().create(request, *args, **kwargs)

        return Response({'error': 'Invalid registration method'},
                        status=status.HTTP_400_BAD_REQUEST)

    # def perform_create(self, serializer):
        # TO DO
