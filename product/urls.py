from django.urls import path
from souparna import views

urlpatterns = [
    path('list/', views.ListAPIView.as_view() , name='product-list')
]