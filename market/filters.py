import django_filters
from django.db.models import Q
from .models import Listing

class ListingFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(method='filter_by_all_titles', label="Szukaj")

    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')

    condition = django_filters.CharFilter(field_name='condition', lookup_expr='exact')

    class Meta:
        model = Listing
        fields = ['condition']

    def filter_by_all_titles(self, queryset, name, value):

        return queryset.filter(
            Q(game__title__icontains=value) |
            Q(custom_title__icontains=value)
        )