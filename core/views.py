from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, Application
from datetime import datetime
from django.http import HttpResponse

def register(request):
    if request.method == 'POST':
        username = request.POST['login']
        password = request.POST['password']
        fio = request.POST['fio']
        phone = request.POST['phone']
        email = request.POST['email']
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Логин занят')
        elif len(username) < 6 or not username.isalnum():
            messages.error(request, 'Логин: минимум 6 символов, только буквы/цифры')
        elif len(password) < 8:
            messages.error(request, 'Пароль не менее 8 символов')
        else:
            user = User.objects.create_user(username=username, password=password,
                                            email=email, fio=fio, phone=phone)
            login(request, user)
            return redirect('index')
    return render(request, 'core/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['login']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Неверный логин или пароль')
    return render(request, 'core/login.html')

def logout_view(request):
    logout(request)
    return redirect('index')

def index(request):
    return render(request, 'core/index.html')

@login_required
def personal(request):
    apps = Application.objects.filter(user=request.user).order_by('-created_at')
    if request.method == 'POST' and 'review' in request.POST:
        app_id = request.POST['app_id']
        text = request.POST['review']
        app = Application.objects.get(id=app_id, user=request.user)
        if app.status == 'Обучение завершено':
            app.review = text
            app.save()
            messages.success(request, 'Отзыв сохранён')
        else:
            messages.error(request, 'Отзыв можно оставить только после окончания курса')
        return redirect('personal')
    return render(request, 'core/personal_account.html', {'applications': apps})

@login_required
def new_application(request):
    if request.method == 'POST':
        course = request.POST['course']
        date_str = request.POST['date']
        payment = request.POST['payment']
        try:
            date_obj = datetime.strptime(date_str, '%d.%m.%Y').date()
            Application.objects.create(
                user=request.user,
                course=course,
                desired_date=date_obj,
                payment_method=payment,
                status='Новая'
            )
            messages.success(request, 'Заявка отправлена')
            return redirect('personal')
        except:
            messages.error(request, 'Ошибка в дате (нужен формат ДД.ММ.ГГГГ)')
    return render(request, 'core/application_form.html')

def admin_panel(request):
    if request.user.username != 'Admin26':
        return HttpResponse('Доступ запрещён', status=403)
    apps = Application.objects.all().order_by('-created_at')
    course_filter = request.GET.get('course_filter')
    if course_filter:
        apps = apps.filter(course=course_filter)
    sort = request.GET.get('sort', '-created_at')
    if sort in ['created_at', '-created_at', 'status', 'course']:
        apps = apps.order_by(sort)
    if request.method == 'POST':
        app_id = request.POST['app_id']
        new_status = request.POST['new_status']
        app = Application.objects.get(id=app_id)
        app.status = new_status
        app.save()
        messages.success(request, 'Статус изменён')
        return redirect('admin_panel')
    context = {
        'applications': apps,
        'courses': Application.objects.values_list('course', flat=True).distinct(),
        'sort': sort,
        'course_filter': course_filter,
    }
    return render(request, 'core/admin_panel.html', context)