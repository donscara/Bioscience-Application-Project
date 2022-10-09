from rest_framework import status

# internal
from .base import BaseTestCase


class ProteinViewsetTestCase(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()

    def test_list_proteins(self):
        endpoint = f"{self.url_api_prefix}proteins/"
        res = self.client.get(endpoint)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res_data = res.json()
        self.assertEqual(res_data.get("count"), 3)
        self.assertEqual(res_data.get("current_page"), 1)
        self.assertEqual(res_data.get("total_pages"), 1)

    def test_list_proteins_filter_by_taxid(self):
        endpoint = f"{self.url_api_prefix}proteins/?taxid={self.tax1.tax_id}"
        res = self.client.get(endpoint)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res_data = res.json()
        self.assertEqual(res_data.get("count"), 2)
        self.assertEqual(res_data.get("current_page"), 1)
        self.assertEqual(res_data.get("total_pages"), 1)

    def test_retrieve_protein(self):
        endpoint = f"{self.url_api_prefix}proteins/{self.protein1.protein_id}/"
        res = self.client.get(endpoint)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res_data = res.json()
        self.assertEqual(
            res_data.get("length_of_sequence"), self.protein1.length_of_sequence
        )
        self.assertEqual(res_data.get("protein_id"), self.protein1.protein_id)
        self.assertEqual(res_data.get("sequence"), self.protein1.sequence)
        self.assertIsNotNone(res_data.get("organism"))
        self.assertIsNotNone(res_data.get("domains"))
        # for domain in res_data.get("domains"):
        #     self.assertTrue(self.protein1.domains.filter(domain_id__in=domain.get('domain_id')))

    def test_post_protein(self):
        protein_id = "A0A034W5F9"
        length_of_sequence = 119
        sequence = "MKPSITSVLFLLATLAGVAIAANSSWGSRNSTNILLLRENVVRSPLKNGYQSVNVDFPKSGQTNTRAISAIFVIDRFTNSSGAYSSLWSGGVGYRFVSLNLKSQYNRGINSTVEIYGKR"
        payload = {
            "length_of_sequence": length_of_sequence,
            "protein_id": protein_id,
            "sequence": sequence,
            "organism": self.organism2.id,
        }
        endpoint = f"{self.url_api_prefix}proteins/"
        res = self.client.post(endpoint, data=payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        res_data = res.json()
        self.assertEqual(res_data.get("length_of_sequence"), length_of_sequence)
        self.assertEqual(res_data.get("protein_id"), protein_id)
        self.assertEqual(res_data.get("sequence"), sequence)
