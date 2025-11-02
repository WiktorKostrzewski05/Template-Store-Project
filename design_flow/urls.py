
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('flowpro/', include('subscription.urls')),
    path('users/', include('users.urls')),
    path('search/', include('search_app.urls')),
    path('cart/', include('cart.urls')),
    path('order/', include('order.urls')),
    path('vouchers/', include('vouchers.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
