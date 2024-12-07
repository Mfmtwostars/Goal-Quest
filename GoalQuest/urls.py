from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from GoalQuest import settings

urlpatterns = [
    path('', include('QuestApp.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
