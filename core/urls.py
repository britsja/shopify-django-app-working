from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.shopify_test, name='shopify_test'),
    path('webhooks/order_updated/', views.order_updated_webhook, name='order_updated_webhook'),
    path('register-webhook/', views.register_webhook),
]