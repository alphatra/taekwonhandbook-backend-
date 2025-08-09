from rest_framework.routers import DefaultRouter
from .views import TechniqueViewSet

router = DefaultRouter()
router.register(r"techniques", TechniqueViewSet, basename="technique")

urlpatterns = router.urls

