from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework import response, status
from django.db.models import F, Sum
from api.filters import ProteinFamilyFilter, ProteinFilter, DomainFilter

# internals
from core.pagiantion import BasePageNumberPagination

from .serializers import (
    DomainDetailedSerializer,
    ProteinDetailedSerializer,
    OrganismSerializer,
    ProteinFamilySerializer,
    ProteinSerializer,
    DomainSerializer,
    TaxonomySerializer,
)
from .models import Organism, Protein, Domain, ProteinFamily, Taxonomy


class ProteinFamilyViewset(viewsets.ModelViewSet):
    serializer_class = ProteinFamilySerializer
    pagination_class = BasePageNumberPagination
    filterset_class = ProteinFamilyFilter
    queryset = ProteinFamily.objects.all().order_by("pf_id")
    lookup_field = "pf_id"


class DomainViewset(viewsets.ModelViewSet):
    serializer_class = DomainSerializer
    pagination_class = BasePageNumberPagination
    filterset_class = DomainFilter
    queryset = Domain.objects.all().order_by("id")

    def get_serializer_class(self):
        if self.action == "retrieve":
            return DomainDetailedSerializer
        return self.serializer_class


class ProteinViewset(viewsets.ModelViewSet):
    serializer_class = ProteinSerializer
    pagination_class = BasePageNumberPagination
    filterset_class = ProteinFilter
    queryset = Protein.objects.all().order_by("protein_id")
    lookup_field = "protein_id"

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ProteinDetailedSerializer
        return self.serializer_class


class CoverageViewset(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    lookup_field = "protein_id"

    def get_coverage(self, protein):
        """Returns sum of all domain stop-start calculation of a protein as dict
        Example of A0A016S8J7 protein's domain start stop values
        (40, 94), (23, 39) => (94-40) + (39-23) = 70
        qs -> {'total_domains': 70}
        """
        qs = protein.domains.annotate(
            total=F("stop_coordinate") - F("start_coordinate")
        ).aggregate(total_domains=Sum("total"))
        res = qs.get("total_domains") / protein.length_of_sequence
        return res

    def retrieve(self, request, protein_id=None):
        try:
            protein = Protein.objects.get(protein_id=protein_id)
            result = self.get_coverage(protein)
            context = {"coverage": result}
            return response.Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            return response.Response(
                {"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


class OrganismViewset(viewsets.ModelViewSet):
    serializer_class = OrganismSerializer
    pagination_class = BasePageNumberPagination
    queryset = Organism.objects.all().order_by("scientific_name")


class TaxonomyViewset(viewsets.ModelViewSet):
    serializer_class = TaxonomySerializer
    pagination_class = BasePageNumberPagination
    queryset = Taxonomy.objects.all().order_by("tax_id")
    lookup_field = "tax_id"
