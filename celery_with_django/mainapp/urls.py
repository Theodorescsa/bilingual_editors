from django.urls import path,include
from . import views
urlpatterns = [
    path('download/', views.download_video_via_url),
    path('generate/', views.generate_subtitle),
]
