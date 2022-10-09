from django.urls import path, include
from rest_framework import routers

# internal
from .views import (
    CoverageViewset,
    OrganismViewset,
    ProteinFamilyViewset,
    ProteinViewset,
    DomainViewset,
    TaxonomyViewset,
)

router = routers.DefaultRouter()


router.register("organisms", OrganismViewset)
router.register("proteins", ProteinViewset)
router.register("domains", DomainViewset)
router.register("protein-families", ProteinFamilyViewset)
router.register("taxonomies", TaxonomyViewset)
router.register("coverage", CoverageViewset, "coverage")


urlpatterns = [path("", include(router.urls))]
