from rest_framework import status

# internal
from .base import BaseTestCase


class DomainViewsetTestCase(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()

    def test_list_domains(self):
        endpoint = f"{self.url_api_prefix}domains/"
        res = self.client.get(endpoint)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res_data = res.json()
        self.assertEqual(res_data.get("count"), 4)
        self.assertEqual(res_data.get("current_page"), 1)
        self.assertEqual(res_data.get("total_pages"), 1)

    def test_list_domains_filter_by_taxid(self):
        endpoint = f"{self.url_api_prefix}domains/?taxid={self.tax1.tax_id}"
        res = self.client.get(endpoint)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res_data = res.json()
        self.assertEqual(res_data.get("count"), 3)
        self.assertEqual(res_data.get("current_page"), 1)
        self.assertEqual(res_data.get("total_pages"), 1)

    def test_retrieve_domain(self):
        endpoint = f"{self.url_api_prefix}domains/{self.domain1.id}/"
        res = self.client.get(endpoint)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res_data = res.json()
        self.assertEqual(
            res_data.get("start_coordinate"), self.domain1.start_coordinate
        )
        self.assertEqual(res_data.get("stop_coordinate"), self.domain1.stop_coordinate)

    def test_post_domain(self):
        start_coord = 10
        stop_coord = 100

        payload = {
            "protein": self.protein3.id,
            "protein_family": self.pfam4.id,
            "start_coordinate": start_coord,
            "stop_coordinate": stop_coord,
        }
        endpoint = f"{self.url_api_prefix}domains/"
        res = self.client.post(endpoint, data=payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        res_data = res.json()
        self.assertEqual(res_data.get("start_coordinate"), start_coord)
        self.assertEqual(res_data.get("stop_coordinate"), stop_coord)
