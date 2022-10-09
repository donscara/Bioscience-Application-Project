from django.db.models import Q
from django_filters.rest_framework import FilterSet, CharFilter, BooleanFilter


class ProteinFilter(FilterSet):
    """Filter class for ProteinViewset to return proteins by given taxonomy id (tax_id)
    Example usage endpoint:
    http://127.0.0.1:8000/api/proteins/?taxid=55661
    """

    taxid = CharFilter(field_name="organism__taxonomy__tax_id", lookup_expr="exact")


class DomainFilter(FilterSet):
    """Filter class for ProteinViewset to return domains by given taxonomy id (tax_id)
    Example usage:
    http://127.0.0.1:8000/api/domains/?taxid=568076
    """

    taxid = CharFilter(
        field_name="protein__organism__taxonomy__tax_id", lookup_expr="exact"
    )

class ProteinFamilyFilter(FilterSet):
    pass