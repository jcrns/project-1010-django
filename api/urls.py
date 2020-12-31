from django.urls import path, include
from . import views
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

router = routers.DefaultRouter()
router.register('get_politician_data', views.GetPoliticianInfo, basename='get_politician_data')
router.register('get_event_data', views.GetEventInfo, basename='get_event_data')
router.register('get_movement_data', views.GetMovementInfo, basename='get_event_data')

urlpatterns = [
    path('', include(router.urls)),
    path('', views.changeProfileData),
]
