from django.urls import path
from .views import *

urlpatterns = [
    # Набор методов для услуг
    path('api/classrooms/search/', search_classrooms),  # 1 GET список с фильтрацией
    path('api/classrooms/<int:classroom_id>/', get_classroom_by_id),  # 2 GET одна запись
    path('api/classrooms/create/', create_classroom), # 3 POST добавление (без изображения)
    path('api/classrooms/<int:classroom_id>/update/', update_classroom),  # 4 PUT изменение
    path('api/classrooms/<int:classroom_id>/delete/', delete_classroom), # 5 DELETE удаление
    path('api/classrooms/<int:classroom_id>/add_to_event/', add_classroom_to_event),  # 6 POST добавления в заявку-черновик.
    path('api/classrooms/<int:classroom_id>/update_image/', update_classroom_image), # 7 POST добавление изображения. 
    # Набор методов для заявок
    #path('api/events/search/', events_list),  # GET список
    path('api/events/<int:event_id>/', get_event_by_id),  # GET одна запись
    path('api/events/<int:event_id>/update/', update_event_by_id),  # PUT изменения полей заявки
    # path('api/events/<int:event_id>/update_status_user/', update_status_user),  # PUT
    # path('api/events/<int:event_id>/update_status_admin/', update_status_admin),  # PUT
    # path('api/events/<int:event_id>/delete/', delete_event),  # DELETE

    # # Набор методов для м-м
    # path('api/events/<int:event_id>/update_classroom/<int:classroom_id>/', update_classroom_in_event),  # PUT
    # path('api/events/<int:event_id>/delete_classroom/<int:classroom_id>/', delete_classroom_from_event),  # DELETE

    # # Набор методов пользователей
    # path('api/users/register/', register), # POST
    # path('api/users/<int:user_id>/update/', update_user), # PUT
]