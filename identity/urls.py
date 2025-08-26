from django.urls import include, path
from rest_framework.routers import DefaultRouter

from identity.views import LogoutView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = "identity"
router = DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
    
    # JWT
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),
    
]
