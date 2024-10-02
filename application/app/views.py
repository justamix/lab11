from django.shortcuts import render, redirect
from app.models import Classrooms, Applications, ApplicationClassrooms
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import connection
from datetime import datetime

def GetClassrooms1(request):
    """АУДИТОРИИ"""
    #обработка поиска
    search_address = request.GET.get('адрес аудитории', '')
    classrooms = Classrooms.objects.filter(address__icontains=search_address, status='active')

    #словарь с данными
    context = {
        'search_address' : search_address,  #запоминание ввода для поиска
        'classrooms' : classrooms           
    }
    #проверка наличия черновика
    draft_booking = GetDraftBooking()
    if draft_booking:
        context['len'] = len(draft_booking.GetClassrooms())
        context['draft_booking'] = draft_booking
    else:
        context['draft_booking'] = None

    return render(request, 'classrooms.html', context)

def GetBooking():
    """Информация об аудиториях в бронировании"""
    draft_booking = GetDraftBooking()
    # Получаем все аудитории, связанные с черновиком заявки
    application_classrooms = ApplicationClassrooms.objects.filter(app=draft_booking)
    classrooms = []
    for item in application_classrooms:
        classroom = {
            'info': Classrooms.objects.get(classroom_id=item.classroom_id),  # Получаем объект аудитории
            'finish_time': item.finish_time.strftime('%H:%M') if item.finish_time else ''# Время окончания
        }
        classrooms.append(classroom)
    return classrooms

def GetCartById(request, id):
    """СТРАНИЦА КОРЗИНЫ"""
    draft_booking = GetDraftBooking()
    context = {
        'id': id,
        'event_name': draft_booking.event_name,
        'fio': draft_booking.creator.username,
        'date': draft_booking.event_date.strftime('%Y-%m-%d') if draft_booking.event_date else '',
        'time_start': draft_booking.start_event_time.strftime('%H:%M') if draft_booking.start_event_time else '',
        'classrooms': GetBooking()
    }

    return render(request, 'cart.html', context)

def GetLongDescription(request, id):
    """ПОДРОБНОЕ ОПИСАНИЕ"""
    classroom = Classrooms.objects.get(classroom_id=id)
    classroom.description = classroom.description.split('t')  
    return render(request, 'long_description.html', { 'classroom' : classroom })

def GetDraftBooking():
    """ПОЛУЧЕНИЕ ЧЕРНОВИКА ЗАЯВКИ"""
    current_user = GetCurrentUser()
    return Applications.objects.filter(creator=current_user.id, status=1).first() #так как у пользователя только один черновик, то берем первый элемент, иначе None

def GetCurrentUser():
    """ВЫБОР ПОЛЬЗОВАТЕЛЯ"""
    return User.objects.filter(is_superuser=False).first()

def AddClassroomToDraftBooking(request, classroom_id):
    """ДОБАВЛЕНИЕ АУДИТОРИИ В ЧЕРНОВИК ЗАЯВКИ"""
    classroom = Classrooms.objects.get(classroom_id=classroom_id)
    draft_booking = GetDraftBooking()
    if draft_booking is None:
        draft_booking = Applications.objects.create(
            created_at=timezone.now(),
            creator=GetCurrentUser(),
            status=1
        )
        draft_booking.save()
    if ApplicationClassrooms.objects.filter(app=draft_booking, classroom=classroom).exists():
        return redirect("/")
    ApplicationClassrooms.objects.create( 
        app=draft_booking,
        classroom=classroom
    )
    return redirect("/")
    
def DeleteBooking(request, booking_id):
    """УДАЛЕНИЕ ЧЕРНОВИКА БРОНИРОВАНИЯ"""
    if request.method == "POST": 
        submitted_time = timezone.now()
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE Applications SET status = 2, submitted_at = %s WHERE app_id = %s",
                [submitted_time, booking_id]
            )
    return redirect("/")