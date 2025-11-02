from django.urls import path
from .views import HomePageView
from . import views

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('templates/', views.temp_list, name='all_templates'),
    path('templates/<uuid:category_id>/<uuid:template_id>/', views.temp_detail, name='template_detail'),
    path('templates/<uuid:category_id>/', views.temp_list, name='templates_by_category'),
]
