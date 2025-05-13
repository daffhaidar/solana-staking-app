from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'wallets', views.WalletViewSet, basename='wallet')
router.register(r'staking', views.StakingViewSet, basename='staking')
router.register(r'prices', views.SolPriceViewSet, basename='price')

urlpatterns = [
    path('', include(router.urls)),
] 