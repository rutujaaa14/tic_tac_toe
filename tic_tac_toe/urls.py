from django.contrib import admin
from django.urls import path, include
from game import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('game.urls')),
    path('api/', include('game.urls')),

]
