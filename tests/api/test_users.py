import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestUserEndpoints:
    def test_get_current_user_unauthenticated(self, api_client):
        url = reverse("user-detail", kwargs={"pk": "me"})
        response = api_client.get(url)

        assert response.status_code == 401

    def test_get_current_user_authenticated(self, authenticated_client, user):
        url = reverse("user-detail", kwargs={"pk": "me"})
        response = authenticated_client.get(url)

        assert response.status_code == 200
        assert response.data["username"] == user.username
        assert response.data["email"] == user.email

    def test_update_current_user(self, authenticated_client, user):
        url = reverse("user-detail", kwargs={"pk": "me"})
        response = authenticated_client.patch(url, {"first_name": "Updated"})

        assert response.status_code == 200
        assert response.data["first_name"] == "Updated"

    def test_delete_user_soft_deletes(self, authenticated_client, user):
        url = reverse("user-detail", kwargs={"pk": "me"})
        response = authenticated_client.delete(url)

        assert response.status_code == 204

        user.refresh_from_db()
        assert user.is_active is False
