from rest_framework import status

# internal
from .base import BaseTestCase


class CoverageViewsetTestCase(BaseTestCase):
    def setUp(self) -> None:
        super().setUp()

    def test_coverage_of_protein(self):
        EXPECTED_COVERAGE = 0.693069306930693
        endpoint = f"{self.url_api_prefix}coverage/{self.protein1.protein_id}/"
        res = self.client.get(endpoint)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        res_data = res.json()
        self.assertEqual(res_data.get("coverage"), EXPECTED_COVERAGE)