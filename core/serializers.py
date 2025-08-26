
from rest_framework import serializers
from .models import Feature, Plan, Subscription


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ["id", "name"]


class PlanSerializer(serializers.ModelSerializer):

    features = FeatureSerializer(many=True, read_only=True)
    feature_ids = serializers.PrimaryKeyRelatedField(
        queryset=Feature.objects.all(), many=True, write_only=True, source="features"
    )

    class Meta:
        model = Plan
        fields = ["id", "name", "features", "feature_ids"]


class SubscriptionSerializer(serializers.ModelSerializer):
    plan = PlanSerializer(read_only=True)
    plan_id = serializers.PrimaryKeyRelatedField(
        queryset=Plan.objects.all(), source="plan", write_only=True
    )

    class Meta:
        model = Subscription
        fields = ["id", "start_date", "is_active", "plan", "plan_id"]

class SubscriptionUpdateSerializer(serializers.ModelSerializer):
    plan_id = serializers.PrimaryKeyRelatedField(
        queryset=Plan.objects.all(), source="plan", write_only=True
    )
    class Meta:
        model = Subscription
        fields = ["plan_id"]
