from typing import Any, Optional
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db import transaction
import random
import decimal
import datetime
import json
import csv

# internal
from api.models import ProteinFamily, Taxonomy, Organism, Protein, Domain


class Command(BaseCommand):
    help = "Read CSV files to store the data in database"

    def read_protein_data(self):
        sequence_dict = {}
        with open("data_sequences.csv", "r") as csv_file:
            seq_reader = csv.reader(csv_file, delimiter=",")
            for row in seq_reader:
                pid = row[0]
                seq = row[1]
                sequence_dict.update({pid: seq})
        with open("data_set.csv", "r") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            for row in csv_reader:
                try:

                    #################
                    protein_id = row[0]
                    tax_id = row[1]
                    clade = row[2]
                    scientific_name = row[3]
                    pfam_description = row[4]
                    pf_id = row[5]
                    start_cord = row[6]
                    stop_cord = row[7]
                    length = row[8]
                    try:
                        tax = Taxonomy.objects.get(tax_id=tax_id)
                    except Taxonomy.DoesNotExist:
                        tax = Taxonomy.objects.create(tax_id=tax_id)
                    try:
                        organism = Organism.objects.get(
                            scientific_name=scientific_name, clade=clade, taxonomy=tax
                        )
                    except Organism.DoesNotExist:
                        organism = Organism.objects.create(
                            scientific_name=scientific_name, clade=clade, taxonomy=tax
                        )
                    try:
                        protein = Protein.objects.get(protein_id=protein_id)
                    except Protein.DoesNotExist:
                        protein = Protein.objects.create(
                            protein_id=protein_id,
                            organism=organism,
                            length_of_sequence=length,
                            sequence=sequence_dict.get(protein_id),
                        )
                    try:
                        protein_family = ProteinFamily.objects.get(pf_id=pf_id)
                    except ProteinFamily.DoesNotExist:
                        protein_family = ProteinFamily.objects.create(
                            pf_id=pf_id, description=pfam_description
                        )
                    try:
                        domain = Domain.objects.get(
                            protein=protein,
                            protein_family=protein_family,
                            start_coordinate=start_cord,
                            stop_coordinate=stop_cord,
                        )
                    except Domain.DoesNotExist:
                        domain = Domain.objects.create(
                            protein=protein,
                            protein_family=protein_family,
                            start_coordinate=start_cord,
                            stop_coordinate=stop_cord,
                        )

                except Exception as e:
                    print(f"{row}\n{e}")

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.stdout.write(self.style.SUCCESS(f"[{start}] Process started..."))
        self.stdout.write(
            self.style.SUCCESS("While storing dataset into database please wait...")
        )
        self.stdout.write(
            self.style.SUCCESS("This can take a few minutes...")
        )
        self.read_protein_data()

        self.stdout.write(
            self.style.WARNING(f"Protein count  : {Protein.objects.count()}")
        )
        self.stdout.write(
            self.style.WARNING(f"Domain count   : {Domain.objects.count()}")
        )
        self.stdout.write(
            self.style.WARNING(f"Organism count : {Organism.objects.count()}")
        )
        self.stdout.write(
            self.style.WARNING(f"ProteinFamily count : {ProteinFamily.objects.count()}")
        )
        self.stdout.write(
            self.style.WARNING(f"Taxonomy count : {Taxonomy.objects.count()}")
        )
        end = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.stdout.write(self.style.SUCCESS(f"[{end}] Process finished..."))
