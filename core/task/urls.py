from django.urls import path
from .views import *

urlpatterns = [
    path('',  dashboard_page ),
    path('dashboard/', dashboard_page, name='dashboard_page'),
    path('addtask/', add_task, name='add_task'),
    path('deletetask/<int:task_id>', delete_task, name='delete_task'),
    path('updatetask/<int:task_id>', update_task, name='update_task'),
    path('calendar/', calendar, name='calendar'),
    path('mytasks/', mytasks, name='mytasks'),
    path('makefavourite/<int:task_id>', makefavourite, name='make_favourite'),
    path('myfavourites/', myfavourites, name='my_favourites'),
    path('removefavourite/<int:task_id>', removefavourite, name='remove_favourite'),
    path('task_details/<id>', task_details , name='task_details'),
    path('delete_comment/<int:task_id>/<int:comment_id>/', delete_comment, name='delete_comment'),
    path('update_comment/<int:task_id>/<int:comment_id>/', update_comment, name='update_comment'),

]
