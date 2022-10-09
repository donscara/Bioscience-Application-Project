from rest_framework import serializers

from .models import Organism, Protein, Domain, ProteinFamily, Taxonomy


class TaxonomySerializer(serializers.ModelSerializer):
    class Meta:
        model = Taxonomy
        fields = ("id", "name", "tax_id")
        lookup_field = "tax_id"


class ProteinFamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProteinFamily
        fields = (
            "id",
            "pf_id",
            "description",
        )

    lookup_field = "pf_id"


class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = (
            "id",
            "protein",
            "protein_family",
            "start_coordinate",
            "stop_coordinate",
        )


class DomainDetailedSerializer(DomainSerializer):
    protein_family = ProteinFamilySerializer()


class OrganismSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organism
        fields = ("id", "scientific_name", "clade", "taxonomy")


class OrganismDetailedSerializer(OrganismSerializer):
    taxonomy = TaxonomySerializer()


class ProteinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Protein
        fields = (
            "id",
            "length_of_sequence",
            "protein_id",
            "sequence",
            "organism",
        )
        # read_only_fields = ['length_of_sequence']


class ProteinDetailedSerializer(ProteinSerializer):
    organism = OrganismDetailedSerializer(read_only=True)
    domains = DomainDetailedSerializer(many=True, read_only=True)

    class Meta(ProteinSerializer.Meta):
        model = Protein
        fields = ProteinSerializer.Meta.fields + ("organism", "domains")
        lookup_field = "protein_id"
