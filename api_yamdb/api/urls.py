from django.urls import include, path
from rest_framework import routers
from .views import give_token, signup

router = routers.DefaultRouter()

urlpatterns = [
    path('v1/auth/token/', give_token),
    path('v1/auth/signup/', signup),
    path('v1/', include(router.urls)),
]