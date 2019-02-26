from rest_framework.routers import DefaultRouter
from bills import views

router = DefaultRouter()
router.register(r'bills', views.BillInformationViewSet, basename="bills")

urlpatterns = router.urls
