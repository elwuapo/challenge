"""
URL configuration for ms1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path

from backend.views import Punch
from backend.views import Person
from backend.views import Report
from backend.views import Check

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Punch
    path('api/v1/punch/', Punch.as_view(), name='punch'),

    # Person
    path('api/v1/person/', Person.as_view(), name='person'),

    # Report
    path('api/v1/report/', Report.as_view(), name='report'),

    # Check
    path('api/v1/check/', Check.as_view(), name='check'),
    # File
    #path('files/', RedirectView.as_view(url=settings.STATIC_URL + '<str:name>')),
    #path('reporte/<path:path>/', serve, {'document_root': settings.STATIC_ROOT}),
]

