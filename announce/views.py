from rest_framework import viewsets
from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import (
    Announce,
    Solicitation
)
from core.models import Entreprise, CustomUser
from .serializers import (
    AnnounceSerializer,
    AnnounceDetailSerializer
)
from utils.result import resultat


# Create your views here.
class AnnounceListAPI(generics.ListAPIView):
    model = Announce
    serializer_class = AnnounceSerializer
    # permission_classes = [IsAuthenticated]
    queryset = Announce.objects.filter(active=True)


class RegisteredAnnounceListAPI(generics.ListAPIView):
    model = Announce
    serializer_class = AnnounceSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # user = self.request.user
        user = CustomUser.objects.get(pk=2)
        try:
            enterprise = Entreprise.objects.get(user=user)
        except ObjectDoesNotExist:
            enterprise = None
        if enterprise is None:
            pass
        return Announce.objects.filter(auteur=enterprise, active=True)


class AnnounceViewSet(viewsets.ModelViewSet):
    """
    Example empty viewset demonstrating the standard
    actions that will be handled by a router class.

    If you're using format suffixes, make sure to also include
    the `format=None` keyword argument for each action.
    """
    queryset = Announce.objects.filter(active=True)
    serializer_class = AnnounceSerializer
    permission_classes = [AllowAny]
    pagination_class = PageNumberPagination

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Announce.objects.filter(active=True)
        announce = get_object_or_404(queryset, pk=pk)
        serializer = AnnounceDetailSerializer(announce)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get'], name='solicit announce')
    def solicited(self, request, pk=None):
        announce = self.get_object()
        user = request.user
        Solicitation.objects.create(announce=announce, user=user)
        result = {
            "status": status.HTTP_200_OK,
            "message" : "Votre sollicitation a été enregistré avec succès"
        }
        return result
