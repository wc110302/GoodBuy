from django.urls import path

from GoodBuy import settings
from app.home.user import user_api
from django.contrib.staticfiles.urls import static

urlpatterns = [
    path(r'user_register/', user_api.user_register, name='user_register'),
    path(r'user_login/', user_api.user_login, name='user_login'),
    path(r'user_logout/', user_api.user_logout, name='user_logout'),
    path(r'user_home/', user_api.user_home, name='user_home'),
    path(r'user_collection/', user_api.user_collection, name='user_collection'),
    path(r'user_comment/', user_api.user_comment, name='user_comment'),
    path(r'user_icon/', user_api.user_icon, name='user_icon'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)