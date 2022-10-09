from rest_framework import status

# internal
from .base import BaseTestCase


class ProteinFamilyViewsetTestCase(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()

    def test_list_protein_family(self):
        endpoint = f"{self.url_api_prefix}protein-families/"
        res = self.client.get(endpoint)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res_data = res.json()
        self.assertEqual(res_data.get("count"), 4)
        self.assertEqual(res_data.get("current_page"), 1)
        self.assertEqual(res_data.get("total_pages"), 1)

    def test_retrieve_protein_family(self):
        endpoint = f"{self.url_api_prefix}protein-families/{self.pfam1.pf_id}/"
        res = self.client.get(endpoint)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res_data = res.json()
        self.assertEqual(
            res_data.get("pf_id"), self.pfam1.pf_id
        )
        self.assertEqual(res_data.get("description"), self.pfam1.description)

    # def test_post_protein_family(self):
    #     # TODO
    #     pass
