from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from core.models import Feature, Plan, Subscription

class TestSubscriptionViewSet(APITestCase):
    @property
    def base_url(self):
        return reverse("subscription-list")

    @classmethod
    def setUpTestData(cls):
        cls.superuser = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="adminpass"
        )
        cls.feature1 = Feature.objects.create(name="Feature 1")
        cls.feature2 = Feature.objects.create(name="Feature 2")
        cls.plan1 = Plan.objects.create(name="Plan 1")
        cls.plan1.features.set([cls.feature1, cls.feature2])
        cls.plan2 = Plan.objects.create(name="Plan 2")
        cls.plan2.features.set([cls.feature1])

    def setUp(self):
        self.client.force_authenticate(user=self.superuser)

    def test_create_subscription(self):
        payload = {"plan_id": self.plan1.id}
        response = self.client.post(self.base_url, payload, format="json")
        assert response.status_code == status.HTTP_201_CREATED, response.data
        assert "id" in response.data
        assert response.data["plan"]["id"] == self.plan1.id

    def test_switch_user_plan(self):
        subscription = Subscription.objects.create(user=self.superuser, plan=self.plan1)
        url = reverse("me-subscription-plan-update", kwargs={"subscription_id": subscription.id})
        payload = {"plan_id": self.plan2.id}
        response = self.client.put(url, payload, format="json")
        assert response.status_code == status.HTTP_200_OK, response.data
        subscription.refresh_from_db()
        assert subscription.plan.id == self.plan2.id

    def test_subscription_list_with_nested_plan_and_features(self):
        Subscription.objects.create(user=self.superuser, plan=self.plan1)
        response = self.client.get(self.base_url)
        assert response.status_code == status.HTTP_200_OK, response.data
        assert response.data["count"] == 1
        sub = response.data["results"][0]
        assert sub["plan"]["name"] == "Plan 1"
        feature_names = [f["name"] for f in sub["plan"]["features"]]
        assert "Feature 1" in feature_names
        assert "Feature 2" in feature_names
