from rest_framework import status
# internal
from .base import BaseTestCase

class TaxonomyViewsetTestCase(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()

    def test_list_taxonomies(self):
        endpoint = f"{self.url_api_prefix}taxonomies/"
        res = self.client.get(endpoint)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res_data = res.json()
        self.assertEqual(res_data.get("count"), 2)
        self.assertEqual(res_data.get("current_page"), 1)
        self.assertEqual(res_data.get("total_pages"), 1)

    def test_retrieve_taxonomy(self):
        endpoint = f"{self.url_api_prefix}taxonomies/{self.tax1.tax_id}/"
        res = self.client.get(endpoint)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res_data = res.json()
        self.assertEqual(res_data.get("tax_id"), self.tax1.tax_id)

    def test_post_taxonomy(self):
        taxonomy_name = ""
        taxonomy_tax_id = "568076"
        payload = {"name": taxonomy_name, "tax_id": taxonomy_tax_id}
        endpoint = f"{self.url_api_prefix}taxonomies/"
        res = self.client.post(endpoint, data=payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        res_data = res.json()
        self.assertEqual(res_data.get("name"), taxonomy_name)
        self.assertEqual(res_data.get("tax_id"), taxonomy_tax_id)
