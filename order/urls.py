from django.urls import path

from .views import OrderView

urlpatterns = [
    path('/product/<int:product_id>',OrderView.as_view())
]
