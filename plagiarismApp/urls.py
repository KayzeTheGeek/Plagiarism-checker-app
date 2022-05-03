from unicodedata import name
from django.urls import path
# now import the views.py file into this code
from .views import Showfile,FileResult
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', Showfile.as_view()),
    # path('result', FileResult.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
