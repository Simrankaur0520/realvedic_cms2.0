from django.urls import path
import admin_realvedic_app.views as views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
                path('adminLogin',views.adminLogin,name='adminLogin'),

              ]+static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)