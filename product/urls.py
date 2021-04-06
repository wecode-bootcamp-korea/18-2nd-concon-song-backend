from django.urls import path

from .views      import ProductDetailView
from .views      import ProductFilterView

urlpatterns = [
    path('/<int:product_id>', ProductDetailView.as_view()),
    path('', ProductFilterView.as_view()),
]