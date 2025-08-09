from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import MediaAssetViewSet, MediaCompleteView, MediaUploadView

urlpatterns = [
    path("media/upload", MediaUploadView.as_view(), name="media-upload"),
    path("media/complete", MediaCompleteView.as_view(), name="media-complete"),
]

router = DefaultRouter()
router.register(r"media", MediaAssetViewSet, basename="mediaasset")

urlpatterns += router.urls

