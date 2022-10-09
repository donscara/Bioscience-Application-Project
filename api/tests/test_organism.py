from rest_framework import status

# internal
from .base import BaseTestCase


class OrganismViewsetTestCase(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()

    def test_list_organisms(self):
        endpoint = f"{self.url_api_prefix}organisms/"
        res = self.client.get(endpoint)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res_data = res.json()
        self.assertEqual(res_data.get("count"), 2)
        self.assertEqual(res_data.get("current_page"), 1)
        self.assertEqual(res_data.get("total_pages"), 1)

    def test_retrieve_organism(self):
        endpoint = f"{self.url_api_prefix}organisms/{self.organism1.id}/"
        res = self.client.get(endpoint)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res_data = res.json()
        self.assertEqual(
            res_data.get("scientific_name"), self.organism1.scientific_name
        )
        self.assertEqual(res_data.get("taxonomy"), self.organism1.taxonomy.id)

    def test_post_organism(self):
        scientific_name = "Metarhizium robertsii"
        clade = "E"
        payload = {
            "scientific_name": scientific_name,
            "clade": clade,
            "taxonomy": self.tax1.id,
        }
        endpoint = f"{self.url_api_prefix}organisms/"
        res = self.client.post(endpoint, data=payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        res_data = res.json()
        self.assertEqual(res_data.get("scientific_name"), scientific_name)
        self.assertEqual(res_data.get("clade"), clade)
