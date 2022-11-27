from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from django.shortcuts import get_object_or_404
from rest_framework import (
    status,
    viewsets,
    generics
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)
from rest_framework.response import Response
from rest_framework.views import APIView

from utils.result import resultat
from utils.TraitementProfile import TraitementProfile
from .serializers import *


# Create your views here.
class GoogleLogin(SocialLoginView): # if you want to use Implicit Grant, use this
    adapter_class = GoogleOAuth2Adapter


class SignUpView(APIView):
    permission_classes = [AllowAny]

    @classmethod
    def post(cls, request):
        email = request.data.get('email')
        email_exist = CustomUser.objects.filter(email=email).exists()
        if email_exist:
            result = resultat(status.HTTP_409_CONFLICT, "Cet email existe déja")
            return Response(result)
        userSerializer = UserSerializer(data=request.data)
        if userSerializer.is_valid():
            userSerializer.save()
            result = resultat(status.HTTP_201_CREATED, userSerializer.data)
            return Response(result)
        else:
            result = resultat(status.HTTP_400_BAD_REQUEST,
                              userSerializer.errors)
            return Response(result)


class InfluenceurView(APIView):

    permission_classes = [AllowAny]

    @classmethod
    def post(cls, request):
        serializer = InfluenceurProfilSerializer(data=request.data)
        if serializer.is_valid():
            user = TraitementProfile().treat_user(request)
            if user is None:
                result = resultat(status.HTTP_400_BAD_REQUEST, "L'utilisateur renseigné n'existe pas")
                return Response(result)
            serializer.save(user=user)
            result = resultat(status.HTTP_201_CREATED, serializer.data)
            return Response(result)
        else:
            result = resultat(status.HTTP_400_BAD_REQUEST, serializer.errors)
            return result


class EnterpriseView(APIView):
    permission_classes = [AllowAny]

    @classmethod
    def post(cls, request):
        serializer = EnterpriseProfileSerializer(data=request.data)
        if serializer.is_valid():
            user = TraitementProfile().treat_user(request)
            if user is None:
                result = resultat(status.HTTP_400_BAD_REQUEST, "L'utilisateur renseigné n'existe pas")
                return Response(result)
            forme = TraitementProfile().treat_forme_juridique(request)
            if forme is None:
                result = resultat(status.HTTP_400_BAD_REQUEST, "Veuillez renseigner une forme juridique")
                return Response(result)
            serializer.save(user=user, forme_juridique=forme)
            result = resultat(status.HTTP_201_CREATED, serializer.data)
            return Response(result)
        else:
            print(serializer.errors)
            pass
    pass


class UserListAPI(generics.ListAPIView):
    model = CustomUser
    serializer_class = UserInfoSerializer
    permission_classes = [IsAuthenticated]
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
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def list(self, request, project_pk=None):
        queryset = self.queryset.filter()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = CustomUser.objects.filter(is_active=True)
        user = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(user)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        instance = self.get_object()
        instance.user.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class InfluenceurViewSet(viewsets.ModelViewSet):
    queryset = Influenceur.objects.filter()
    serializer_class = InfluenceurProfilSerializer
    permission_classes = [AllowAny]

    def retrieve(self, request, pk=None):
        queryset = Influenceur.objects.filter()
        user = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(user)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        pass


class EnterpriseViewSet(viewsets.ModelViewSet):
    queryset = Entreprise.objects.filter()
    serializer_class = EnterpriseProfileSerializer
    permission_classes = [AllowAny]

    def retrieve(self, request, pk=None):
        queryset = Entreprise.objects.filter()
        user = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(user)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        pass
