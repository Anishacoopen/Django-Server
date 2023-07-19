"""
URL configuration for DisasterDetection project.

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
#from django.contrib import admin
#from django.urls import path

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Import the path for the view 'detection_page'
from detection_page.views import image_upload_view,classify_image, back_button


urlpatterns = [
    path("admin/", admin.site.urls),

    #Add an url for the view
    path("Detection/", image_upload_view),
    #Add an url for the view
    path("Classify/", classify_image , name = 'classify_image'),

       #Add an url for the view
    path('', back_button, name='home_detection'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
