from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView

from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import viewsets
from rest_framework import status
from rest_framework import generics

from core import serializers
from core.serializers import SubscriptionSerializer, SubscriptionUpdateSerializer
from rest_framework import permissions
from core.models import Feature, Plan
from core.serializers import FeatureSerializer, PlanSerializer
from drf_spectacular.utils import extend_schema, OpenApiResponse
from drf_spectacular.types import OpenApiTypes
from core.models import Subscription  # Import Subscription model


class FeatureViewSet(viewsets.ModelViewSet):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer
    permission_classes = [permissions.IsAdminUser]

class PlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.prefetch_related("features").all()
    serializer_class = PlanSerializer
    permission_classes = [permissions.IsAdminUser]


class SubscriptionViewSet(viewsets.GenericViewSet, viewsets.mixins.ListModelMixin, viewsets.mixins.CreateModelMixin):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Subscription.objects.filter(user=self.request.user)
            .select_related("plan")
            .prefetch_related("plan__features")
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



@extend_schema(
    responses={
        200: OpenApiResponse(
             response=None,
            description="Plan updated successfully. Returns a message."
        )
    }
)
class MySubscriptionPlanUpdateView(generics.UpdateAPIView):
    serializer_class = SubscriptionUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_url_kwarg = "subscription_id"

    def update(self, request, *args, **kwargs):
        subscription_id = self.kwargs.get(self.lookup_url_kwarg)
        subscription = get_object_or_404(Subscription, id=subscription_id, user=request.user)
        serializer = self.get_serializer(subscription, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # Return a success message
        return Response(
            {"message": "Plan updated successfully."},
            status=status.HTTP_200_OK
        )