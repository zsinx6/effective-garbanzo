from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from records.urls import router as recordsrouter
from bills.urls import router as billsrouter

router = DefaultRouter()
router.registry.extend(recordsrouter.registry)
router.registry.extend(billsrouter.registry)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
