from django.urls import path, include
from rest_framework.routers import DefaultRouter

from core.views import MySubscriptionPlanUpdateView, SubscriptionViewSet, PlanViewSet, FeatureViewSet

router = DefaultRouter()
router.register(r'me/subscriptions', SubscriptionViewSet, basename='subscription')
path("me/subscription/<int:subscription_id>/plan/", MySubscriptionPlanUpdateView.as_view(), name="me-subscription-plan-update"),
router.register(r'plans', PlanViewSet, basename='plan')
router.register(r'features', FeatureViewSet, basename='feature')

urlpatterns = [
    path("me/subscription/<int:subscription_id>/plan/", MySubscriptionPlanUpdateView.as_view(), name="me-subscription-plan-update"),
    path('', include(router.urls)),
    
]