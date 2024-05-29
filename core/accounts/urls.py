from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login_page, name='login_page'),
    path('register/', register_page, name='register_page'),
    path('logout/', logout_page, name='logout'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('update_profile_picture/', update_profile_picture, name='update_profile_picture'),
    path('update_profile_details/', update_profile_details, name='update_profile_details'),
]