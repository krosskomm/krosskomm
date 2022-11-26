from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import (
    exceptions,
    status,
    serializers,
    viewsets,
    generics
)
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from utils.result import resultat
from .models import *
from .serializers import *
# from .influenceur.profile import *
from rest_framework.pagination import PageNumberPagination


# Create your views here.
class UserListAPI(generics.ListAPIView):
    model = CustomUser
    serializer_class = UserInfoSerializer
    permission_classes = [AllowAny]
    queryset = CustomUser.objects.filter(is_active=True, is_staff=False)


class UserViewSet(viewsets.ModelViewSet):
    """
    Example empty viewset demonstrating the standard
    actions that will be handled by a router class.

    If you're using format suffixes, make sure to also include
    the `format=None` keyword argument for each action.
    """
    queryset = CustomUser.objects.filter(is_active=True)
    serializer_class = UserInfoSerializer
    permission_classes = [AllowAny]
    pagination_class = PageNumberPagination

    def list(self, request, project_pk=None):
        queryset = self.queryset.filter()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        pass

    def retrieve(self, request, pk=None):
        print('quest ce que tu fais la ')
        queryset = CustomUser.objects.filter(is_active=True)
        user = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(user)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        instance = self.get_object()
        instance.user.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
