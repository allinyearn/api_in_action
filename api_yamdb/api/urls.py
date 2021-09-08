from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView, TokenVerifyView,
)
from .views import signup

router = routers.DefaultRouter()
# router.register(r'users', UsersViewSet, basename='users')

# свои эндпоинты к АПИ добавляем сюда
# или роутерами или прямым маршрутом по аналогии)

urlpatterns = [
    path('v1/auth/token/', TokenObtainPairView.as_view()),
    path('v1/auth/signup/', signup),
    path('v1/', include(router.urls)),
]