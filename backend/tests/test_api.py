import json
import pytest
from django.test import Client
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

from tkh_lexicon.models import Technique
from tkh_patterns.models import Tul


@pytest.mark.django_db
def test_health_ok_or_degraded():
    c = Client()
    resp = c.get("/health/")
    assert resp.status_code == 200
    assert resp.json()["status"] in ("ok", "degraded")


@pytest.mark.django_db
def test_schema_available():
    c = Client()
    resp = c.get("/api/schema/")
    assert resp.status_code == 200


@pytest.mark.django_db
def test_techniques_list_and_detail():
    c = Client()
    # empty list
    resp = c.get("/api/v1/techniques/")
    assert resp.status_code == 200
    data = resp.json()
    # paginated structure
    assert "results" in data

    # create one
    Technique.objects.create(
        names={"pl": "Ap Chagi", "en": "Front Kick", "kr": "앞차기"},
        category="kick",
        min_belt=7,
        key_points=["prostuj kolano"],
        videos={"front": "https://example.com/front.mp4"},
        tags=["fundamentals"],
    )

    resp = c.get("/api/v1/techniques/")
    assert resp.status_code == 200
    assert resp.json()["count"] >= 1

    resp = c.get("/api/v1/techniques/1/")
    assert resp.status_code == 200
    data = resp.json()
    assert data["category"] == "kick"


@pytest.mark.django_db
def test_tuls_list():
    c = Client()
    Tul.objects.create(name="Chon-Ji", belt=9, steps=["s1", "s2"], videos={})
    resp = c.get("/api/v1/tuls/")
    assert resp.status_code == 200
    assert resp.json()["count"] >= 1


@pytest.mark.django_db
def test_progress_upsert_jwt():
    User = get_user_model()
    user = User.objects.create_user(username="tester", password="pass123")
    access = str(RefreshToken.for_user(user).access_token)
    c = Client(HTTP_AUTHORIZATION=f"Bearer {access}")

    # create
    resp = c.post(
        "/api/v1/progress/",
        data={"item_type": "technique", "item_id": 1, "status": "seen", "score": 0.5, "streaks": 2},
    )
    assert resp.status_code in (200, 201)
    # list
    resp = c.get("/api/v1/progress/")
    assert resp.status_code == 200
    payload = resp.json()
    assert payload["count"] >= 1
    assert payload["results"][0]["item_type"] == "technique"

