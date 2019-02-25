from rest_framework.routers import DefaultRouter
from records import views

router = DefaultRouter()
router.register(r'records', views.CallRecordViewSet, basename="records")

urlpatterns = router.urls
