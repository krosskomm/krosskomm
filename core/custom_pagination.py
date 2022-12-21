from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from core.models import Influenceur


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        user = self.request.user
        try:
            influenceur = Influenceur.objects.get(user=user)
        except ObjectDoesNotExist:
            influenceur = None
        if influenceur is None:
            saved = []
        else:
            saved = influenceur.solicitations.filter(solicitation__is_favorite=True).values_list('id', flat=True)

        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'saved': list(saved),
            'results': data,
        })
