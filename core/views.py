from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework import (
    status,
    viewsets,
    generics
)
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)
from rest_framework.response import Response
from rest_framework.views import APIView
from contrat.models import Contrat
from utils.result import resultat
from utils.TraitementProfile import TraitementProfile
from utils.badge import badge_verification_save
from .serializers import *
from announce.serializers import AnnounceSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
import datetime


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# Create your views here.
class GoogleLogin(SocialLoginView):  # if you want to use Implicit Grant, use this
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


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = PasswordSerializer
    model = CustomUser
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                result = resultat(status.HTTP_400_BAD_REQUEST, "Vous avez rentré le mauvais mot de passe.")
                return Response(result)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            result = resultat(status.HTTP_200_OK, 'Mot de passe modifié avec succès')
            return Response(result)
        else:
            result = resultat(status.HTTP_400_BAD_REQUEST, serializer.errors)
            return Response(result)


class ChangeEmailView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = EmailSerializer
    model = CustomUser
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old email
            if str(self.object.email) == str(serializer.data.get("old_email")):
                new_email = str(serializer.data.get("new_email"))
                if CustomUser.objects.filter(email=str(new_email)).exists():
                    result = resultat(status.HTTP_409_CONFLICT, "Cette adresse mail est déja prise")
                    return Response(result)
                self.object.email = serializer.data.get("new_email")
                self.object.save()
            result = resultat(status.HTTP_200_OK, 'Votre email a été modifié avec succès')
            return Response(result)
        else:
            result = resultat(status.HTTP_400_BAD_REQUEST, serializer.errors)
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
            # active user
            user.is_active = True
            user.save()
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
            user.is_active = True
            user.save()
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


class PaysViewSet(viewsets.ModelViewSet):
    """
    Example empty viewset demonstrating the standard
    actions that will be handled by a router class.

    If you're using format suffixes, make sure to also include
    the `format=None` keyword argument for each action.
    """
    queryset = Pays.objects.filter(active=True)
    serializer_class = PaysSerializer
    permission_classes = [AllowAny]

    def list(self, request, project_pk=None):
        queryset = self.queryset.filter()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class ReputationViewSet(viewsets.ModelViewSet):
    """
    Example empty viewset demonstrating the standard
    actions that will be handled by a router class.

    If you're using format suffixes, make sure to also include
    the `format=None` keyword argument for each action.
    """
    queryset = Reputation.objects.filter(active=True)
    serializer_class = ReputationSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, project_pk=None):
        queryset = self.queryset.filter()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class SecteurViewSet(viewsets.ModelViewSet):
    """
    Example empty viewset demonstrating the standard
    actions that will be handled by a router class.

    If you're using format suffixes, make sure to also include
    the `format=None` keyword argument for each action.
    """
    queryset = SecteurActivite.objects.filter(active=True)
    serializer_class = SecteurSerializer
    permission_classes = [AllowAny]

    def list(self, request, project_pk=None):
        queryset = self.queryset.filter()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class FormeJuridiqueViewSet(viewsets.ModelViewSet):
    """
    Example empty viewset demonstrating the standard
    actions that will be handled by a router class.

    If you're using format suffixes, make sure to also include
    the `format=None` keyword argument for each action.
    """
    queryset = FormeJuridique.objects.filter(active=True)
    serializer_class = FormeJuridiqueSerializer
    permission_classes = [AllowAny]

    def list(self, request, project_pk=None):
        queryset = self.queryset.filter()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class TypeInfleunceurViewSet(viewsets.ModelViewSet):
    """
    Example empty viewset demonstrating the standard
    actions that will be handled by a router class.

    If you're using format suffixes, make sure to also include
    the `format=None` keyword argument for each action.
    """
    queryset = TypeInfluenceur.objects.filter(active=True)
    serializer_class = TypeInfluenceurSerializer
    permission_classes = [AllowAny]

    def list(self, request, project_pk=None):
        queryset = self.queryset.filter()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class ReseauViewSet(viewsets.ModelViewSet):
    """
    Example empty viewset demonstrating the standard
    actions that will be handled by a router class.

    If you're using format suffixes, make sure to also include
    the `format=None` keyword argument for each action.
    """
    queryset = Reseaux.objects.filter(active=True)
    serializer_class = ReseauSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, project_pk=None):
        queryset = self.queryset.filter()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


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

    @action(methods=['POST'], detail=True, name='badge_verification')
    def badge_verification(self, request, *args, **kwargs):
        result = None
        user = self.get_object()
        serializer = UserInfoSerializer(user)
        if serializer.data['entreprise'] is not None:
            profil = Entreprise.objects.get(user=user)
            result = badge_verification_save(profil, request)
        if serializer.data['influenceur'] is not None:
            profil = Influenceur.objects.get(user=user)
            result = badge_verification_save(profil, request)
        return Response(result)

    @action(methods=['GET'], detail=True, name='close_account')
    def close_account(self, request, *args, **kwargs):
        user = self.get_object()
        pass


class InfluenceurViewSet(viewsets.ModelViewSet):
    queryset = Influenceur.objects.filter()
    serializer_class = InfluenceurProfilSerializer
    permission_classes = [IsAuthenticated]

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

    def partial_update(self, request, pk=None):
        instance = self.get_object()
        avatar = request.FILES.get('avatar')
        if avatar:
            instance.avatar = avatar
            instance.save()
        serializer = self.serializer_class(instance)
        return Response(serializer.data)

    @action(detail=True, methods=['PATCH'], name='update social network')
    def update_social_network(self, request, pk=None):
        influenceur = self.get_object()
        reseaux = request.data.get('reseaux')
        if len(reseaux) > 0:
            ReseauxSociaux.objects.filter(influenceur=influenceur).delete()
            for reseau in reseaux:
                try:
                    social = Reseaux.objects.get(pk=int(reseau["reseau"]))
                except ObjectDoesNotExist:
                    social = None
                if social is not None:
                    ReseauxSociaux.objects.create(influenceur=influenceur,
                                                  reseau_social=social,
                                                  lien_url=reseau["lien_url"])
        serializer = InfluenceurProfilSerializer(influenceur)
        return Response(serializer.data)

    @action(detail=True, methods=['PATCH'], name='update languages and place')
    def update_language_place(self, request, pk=None):
        influenceur = self.get_object()
        languages = request.data.get('languages')
        places = request.data.get('places')
        if len(languages) > 0:
            influenceur.languages.clear()
            for id_language in languages:
                try:
                    language = Language.objects.get(pk=int(id_language))
                except ObjectDoesNotExist:
                    language = None
                if language is not None:
                    influenceur.languages.add(language)

        if len(places) > 0:
            influenceur.places.clear()
            for id_country in places:
                try:
                    place = Pays.objects.get(code=str(id_country))
                except ObjectDoesNotExist:
                    place = None
                if place is not None:
                    influenceur.places.add(place)
        serializer = InfluenceurProfilSerializer(influenceur)
        return Response(serializer.data)

    @action(detail=True, methods=['POST'], name='solicited entreprise')
    def solicited_entreprise(self, request, pk=None):
        influenceur = self.get_object()
        id_entreprise = request.data['entreprise']
        try:
            entreprise = Entreprise.objects.get(pk=int(id_entreprise))
        except ObjectDoesNotExist:
            result = {
                "status": status.HTTP_409_CONFLICT,
                "message": "Cette entreprise n'existe pas"
            }
            return Response(result)
        if SimpleSolicitation.objects.filter(entreprise=entreprise, influenceur=influenceur).exists():
            result = {
                "status": status.HTTP_409_CONFLICT,
                "message": "Vous avez déja sollicité cet entreprise"
            }
            return Response(result)
        SimpleSolicitation.objects.create(entreprise=entreprise, influenceur=influenceur,
                                          type_sollicitation="INFLUENCEUR")
        result = {
            "status": status.HTTP_200_OK,
            "message": "Votre solicitation a été envoyée avec succès"
        }
        return Response(result)

    @action(detail=True, methods=['GET'], name='list entreprise solicited')
    def list_solicitation_entreprises(self, request, pk=None):
        influenceur = self.get_object()
        entreprises = influenceur.sollicitations.filter(simplesolicitation__type_sollicitation="INFLUENCEUR")
        serializer = EntrepriseSerializer(entreprises, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['GET'], name='list announces solicited')
    def list_announce_solicited(self, request, pk=None):
        influenceur = self.get_object()
        announces = influenceur.solicitations.filter()
        serializer = AnnounceSerializer(announces, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['GET'], name='list saved announce')
    def list_saved_announces(self, request, pk=None):
        influenceur = self.get_object()
        announces = influenceur.solicitations.filter(solicitation__is_favorite=True)
        serializer = AnnounceSerializer(announces, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['GET'], name='contract number')
    def contract_number(self, request, pk=None):
        today = datetime.date.today()
        influenceur = self.get_object()
        end_contract = influenceur.contrat_set.filter(date_fin__lt=today).count()
        in_progress_contract = influenceur.contrat_set.filter(date_fin__gte=today).count()
        inf_registered = influenceur.solicitations.filter(solicitation__is_favorite=True).count()
        result = {
            "end_contract": end_contract,
            "in_progress_contract": in_progress_contract,
            "registered_number": inf_registered
        }
        return Response(result)


class EnterpriseViewSet(viewsets.ModelViewSet):
    queryset = Entreprise.objects.filter()
    serializer_class = EnterpriseProfileSerializer
    permission_classes = [IsAuthenticated]

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
        instance = self.get_object()
        avatar = request.FILES.get('avatar')
        if avatar:
            instance.avatar = avatar
            instance.save()
        serializer = self.serializer_class(instance)
        return Response(serializer.data)

    @action(detail=True, methods=['POST'], name='solicit influenceur')
    def solicited_influenceur(self, request, pk=None):
        entreprise = self.get_object()
        id_influenceur = request.data['influenceur']
        try:
            influenceur = Influenceur.objects.get(pk=int(id_influenceur))
        except ObjectDoesNotExist:
            result = {
                "status": status.HTTP_409_CONFLICT,
                "message": "Cet influenceur n'existe pas"
            }
            return Response(result)
        if SimpleSolicitation.objects.filter(entreprise=entreprise, influenceur=influenceur).exists():
            result = {
                "status": status.HTTP_409_CONFLICT,
                "message": "Vous avez déja sollicité cet influenceur"
            }
            return Response(result)
        SimpleSolicitation.objects.create(entreprise=entreprise, influenceur=influenceur,
                                          type_sollicitation="ENTREPRISE")
        result = {
            "status": status.HTTP_200_OK,
            "message": "Votre solicitation a été envoyée avec succès"
        }
        return Response(result)

    @action(detail=True, methods=['GET'], name='list influenceur solicited')
    def list_solicitation_influenceurs(self, request, pk=None):
        entreprise = self.get_object()

        influenceurs = entreprise.sollicitations.filter(simplesolicitation__type_sollicitation="ENTREPRISE")
        serializer = InfluenceurSerializer(influenceurs, many=True)
        return Response(serializer.data)


class LanguageViewSet(viewsets.ModelViewSet):
    queryset = Language.objects.filter()
    serializer_class = LanguageSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.filter()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        queryset = CustomUser.objects.filter(is_active=True)
        language = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(language)
        return Response(serializer.data)