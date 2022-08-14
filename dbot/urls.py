import sys
from django.contrib import admin
from django.urls import path, include
from .api.routes import router

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('', include('webapp.urls')),

]
