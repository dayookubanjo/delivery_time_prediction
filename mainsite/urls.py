from django.urls import path , include
from . import views
from django.conf.urls.static import static
from django.conf import  settings

urlpatterns = [
    path("", views.index, name= "index"),
    path("prediction/", views.predict, name= "predict"),

    

]

handler404 = 'mainsite.views.error_404'

# urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)