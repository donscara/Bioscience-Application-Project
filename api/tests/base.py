from django.test import TestCase
from rest_framework.test import APIClient
import random

from api.models import ProteinFamily, Taxonomy, Protein, Organism, Domain


class BaseTestCase(TestCase):
    url_api_prefix = "/api/"

    def setUp(self) -> None:
        self.client = APIClient()
        self.create_taxonomy()  # 1
        self.create_organism()  # 2
        self.create_protein()  # 3
        self.create_protein_family()  # 4
        self.create_domain()  # 5

    def create_taxonomy(self):
        self.tax1 = Taxonomy.objects.create(tax_id=f"53326")
        self.tax2 = Taxonomy.objects.create(tax_id=f"4155")

    def create_organism(self):
        self.organism1 = Organism.objects.create(
            scientific_name=f"Ancylostoma ceylanicum", clade="E", taxonomy=self.tax1
        )
        self.organism2 = Organism.objects.create(
            scientific_name=f"Erythranthe guttata", clade="E", taxonomy=self.tax2
        )

    def create_protein(self):
        self.protein1 = Protein.objects.create(
            protein_id="A0A016S8J7",
            sequence="MVIGVGFLLVLFSSSVLGILNAGVQLRIEELFDTPGHTNNWAVLVCTSRFWFNYRHVSNVLALYHTVKRLGIPDSNIILMLAEDVPCNPRNPRPEAAVLSA",
            length_of_sequence=101,
            organism=self.organism1,
        )
        self.protein2 = Protein.objects.create(
            protein_id="A0A022QDW2",
            sequence="PAHGVPKGFLAVYVEPELRRFIIPMSYLSDPLFKVLLAKAEEEFGFDHSGGLTIPCEIETFKYLLHCMENHRRELSHET",
            length_of_sequence=79,
            organism=self.organism2,
        )
        self.protein3 = Protein.objects.create(
            protein_id="A0A016SK08",
            sequence="METTLFNAPINIPVSKGVKQGDTISPKLFSAGLEMVIRKLNLEKGINIDGEHLTHLRFADDLVLPGEDADTVQKMLRELEIEGRKVGLKINRLKTKIMRSHCAPKMTITLKGEIIEEGGSYVYLGQGVNTSNDLTDGISRRRKAGWLKFNEEKEILLSKTDPKRKAEIFNKTVLPAMIYGCETWAPTKVEERKL",
            length_of_sequence=194,
            organism=self.organism1,
        )

    def create_protein_family(self):
        self.pfam1 = ProteinFamily.objects.create(
            pf_id="PF01650",
            description="Peptidase C13 legumain",
        )
        self.pfam2 = ProteinFamily.objects.create(
            pf_id="PF02931",
            description="Neurotransmitter-gated ion-channel ligand-binding domain",
        )
        self.pfam3 = ProteinFamily.objects.create(
            pf_id="PF02519",
            description="Small auxin-up RNA",
        )
        self.pfam4 = ProteinFamily.objects.create(
            pf_id="PF00078",
            description="Reverse transcriptase domain",
        )

    def create_domain(self):
        self.domain1 = Domain.objects.create(
            protein_family=self.pfam1,
            start_coordinate=40,
            stop_coordinate=94,
            protein=self.protein1,
        )
        self.domain2 = Domain.objects.create(
            protein_family=self.pfam2,
            start_coordinate=23,
            stop_coordinate=39,
            protein=self.protein1,
        )
        self.domain3 = Domain.objects.create(
            protein_family=self.pfam3,
            start_coordinate=4,
            stop_coordinate=67,
            protein=self.protein2,
        )
        self.domain4 = Domain.objects.create(
            protein_family=self.pfam4,
            start_coordinate=10,
            stop_coordinate=99,
            protein=self.protein3,
        )
