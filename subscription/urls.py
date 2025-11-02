from django.urls import path
from . import views

urlpatterns = [
    path('', views.FlowPro, name='FlowPro'),
    path('subscribed/', views.SubscribedView.as_view(), name='subscribed'),

]
