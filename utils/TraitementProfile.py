from core.models import (
    CustomUser, FormeJuridique
)


class TraitementProfile():
    def __init__(self):
        pass

    @staticmethod
    def treat_user(request):
        usr = request.data.get('user')
        try:
            user = CustomUser.objects.get(pk=int(usr))
        except CustomUser.DoesNotExist:
            user = None

        return user

    @staticmethod
    def treat_forme_juridique(request):
        forme = request.data.get('forme_juridique')
        try:
            form_juridique = FormeJuridique.objects.get(pk=int(forme))
        except CustomUser.DoesNotExist:
            form_juridique = None

        return form_juridique
