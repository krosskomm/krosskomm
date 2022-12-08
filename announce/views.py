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
from core.models import Entreprise, Influenceur
from .serializers import (
    AnnounceSerializer,
    AnnounceDetailSerializer
)
from utils.result import resultat


# Create your views here.
class AnnounceListAPI(generics.ListAPIView):
    model = Announce
    serializer_class = AnnounceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Announce.objects.filter(active=True)
        title = self.request.query_params.get('title', None)
        if title:
            queryset = Announce.objects.filter(titre__icontains=title, active=True)
        return queryset


class RegisteredAnnounceListAPI(generics.ListAPIView):
    model = Announce
    serializer_class = AnnounceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        try:
            enterprise = Entreprise.objects.get(user=user)
        except ObjectDoesNotExist:
            enterprise = None
        if enterprise is None:
            result = {
                "status": status.HTTP_404_NOT_FOUND,
                "message": "Cette entreprise n'existe pas"
            }
            return Response(result)
        queryset = Announce.objects.filter(auteur=enterprise, active=True)
        title = self.request.query_params.get('title', None)
        if title:
            queryset = Announce.objects.filter(auteur=enterprise, titre__icontains=title, active=True)
        return queryset


class AnnounceViewSet(viewsets.ModelViewSet):
    """
    Example empty viewset demonstrating the standard
    actions that will be handled by a router class.

    If you're using format suffixes, make sure to also include
    the `format=None` keyword argument for each action.
    """
    queryset = Announce.objects.filter(active=True)
    serializer_class = AnnounceSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.filter()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        id_entreprise = request.POST.get('auteur', None)
        print("")
        if id_entreprise is not None:
            try:
                entreprise = Entreprise.objects.get(pk=int(id_entreprise))
            except ObjectDoesNotExist:
                entreprise = None
            print(entreprise)
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(auteur=entreprise)
            if request.FILES.get('cover') is not None:
                serializer.cover = request.FILES.get('cover')
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

    @action(detail=True, methods=['POST'], name='solicit announce')
    def solicited(self, request, pk=None):
        announce = self.get_object()
        id_influenceur = request.data['influenceur']
        try:
            influenceur = Influenceur.objects.get(pk=int(id_influenceur))
        except ObjectDoesNotExist:
            result = {
                "status": status.HTTP_409_CONFLICT,
                "message": "Cet influenceur n'existe pas"
            }
            return Response(result)

        try:
            solicitation = Solicitation.objects.get(announce=announce, influenceur=influenceur)
        except ObjectDoesNotExist:
            solicitation = None
        if solicitation is not None:
            result = {
                "status": status.HTTP_409_CONFLICT,
                "message": "Vous avez déja solliciter cette annonce"
            }
            return Response(result)
        Solicitation.objects.create(announce=announce, influenceur=influenceur)
        result = {
            "status": status.HTTP_200_OK,
            "message": "solicitation enregistrée avec succès"
        }
        return Response(result)



