from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, MaterialViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('materials', MaterialViewSet)

urlpatterns = [
    path('', include(router.urls))
]