from celery import shared_task
from .models import MediaAsset
import os


@shared_task
def transcode_media(media_id: int) -> None:
    try:
        asset = MediaAsset.objects.get(id=media_id)
    except MediaAsset.DoesNotExist:
        return
    # Placeholder: w realu wywołanie ffmpeg, generacja miniatur, update pól
    asset.status = "ready"
    asset.resolutions = ["480p"]
    # Umieść miniaturę w tym samym katalogu co plik źródłowy
    dirpath = os.path.dirname(asset.file) if asset.file else ""
    thumb_name = "thumb_0001.jpg"
    asset.thumbnails = [f"{dirpath}/{thumb_name}" if dirpath else thumb_name]
    asset.save(update_fields=["status", "resolutions", "thumbnails"])

