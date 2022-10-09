from django.db import models

from core.models import Base


class Taxonomy(Base):
    """This is the Taxonomy model"""

    name = models.CharField(max_length=280, null=True, blank=True)
    tax_id = models.CharField(max_length=120)

    class Meta:
        db_table = "t_taxonomy"

    def __str__(self) -> str:
        return self.tax_id


class Organism(Base):
    """This is the Organism model"""

    scientific_name = models.CharField(max_length=280, unique=True)
    clade = models.CharField(max_length=1)
    taxonomy = models.ForeignKey(Taxonomy, on_delete=models.CASCADE)

    class Meta:
        db_table = "t_organism"

    def __str__(self) -> str:
        return self.scientific_name


class Protein(Base):
    protein_id = models.CharField(max_length=120, unique=True)
    sequence = models.TextField(null=True, blank=True)
    organism = models.ForeignKey(
        Organism, on_delete=models.CASCADE, related_name="proteins"
    )
    length_of_sequence = models.PositiveIntegerField()

    class Meta:
        db_table = "t_protein"

    def __str__(self) -> str:
        return self.protein_id

    # def save(self, *args, **kwargs):
    #     self.length_of_sequence = len(self.sequence)
    #     return super().save(*args, **kwargs)


class ProteinFamily(Base):
    pf_id = models.CharField(max_length=120, unique=True)
    description = models.TextField()

    class Meta:
        db_table = "t_protein_family"

    def __str__(self) -> str:
        return self.pf_id


class Domain(Base):
    """Protein Family"""

    protein = models.ForeignKey(
        Protein, on_delete=models.CASCADE, related_name="domains"
    )
    protein_family = models.ForeignKey(ProteinFamily, on_delete=models.CASCADE)
    start_coordinate = models.IntegerField()
    stop_coordinate = models.IntegerField()

    class Meta:
        db_table = "t_domain"
        unique_together = (
            "protein",
            "protein_family",
            "start_coordinate",
            "stop_coordinate",
        )

    def __str__(self) -> str:
        return self.protein_family.pf_id
