import sys
from django.contrib import admin
from django.urls import path, include
from .api.routes import router
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('messages/', views.messages),
]
