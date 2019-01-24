from django.urls import path, include
from rest_framework.routers import DefaultRouter
from records import views

router = DefaultRouter()
router.register(r'records', views.CallRecordViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
