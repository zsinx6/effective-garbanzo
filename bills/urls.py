from django.urls import path, include
from rest_framework.routers import DefaultRouter
from bills import views

router = DefaultRouter()
router.register(r'bills', views.BillInformationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
