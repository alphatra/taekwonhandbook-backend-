from rest_framework.routers import DefaultRouter
from .views import TulViewSet

router = DefaultRouter()
router.register(r"tuls", TulViewSet, basename="tul")

urlpatterns = router.urls

