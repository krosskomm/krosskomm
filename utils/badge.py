from utils.result import resultat
from rest_framework import (
    status
)
from core.models import Badge


def badge_verification_save(profil, request):
    if profil.badge_verification:
        result = resultat(status.HTTP_409_CONFLICT, "Votre compte a été déja activé")
        return result

    badge = Badge.objects.create(identity_recto=request.FILES.get('identity_recto'),
                                 identity_verso=request.FILES.get('identity_verso'),
                                 selfie=request.FILES.get('selfie'))
    profil.badge = badge
    profil.badge_verification = True
    profil.save()
    result = resultat(status.HTTP_200_OK, "Votre compte a été vérifié avec succès")
    return result
