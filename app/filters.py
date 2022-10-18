import django_filters
from .models import Constat


class ContratFilter(django_filters.FilterSet):
    class Meta:
        model = Constat
        fields=['telephone','immatriculation']
