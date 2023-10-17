from django.shortcuts import render

#TEST
# from django.http import HttpResponse

# def index(request):
#     return HttpResponse("TEST")
# def showtemplate(request):
#     return render(request, 'list.html')
from .models import Order
from django.shortcuts import redirect
from datetime import timedelta
from dateutil import parser
import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth import authenticate, login, logout
from .models import ConfeRoom, Order
from django.contrib import messages
from .forms import Logi_form, Register_form, Add_form
from .models import Event
from .forms import EventForm
from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone

#顯示可用的會議室
def list(request):
    room = ConfeRoom.objects.all()
    content = {
        'room': room
    }
    return render(request, 'list.html', content)

#某個會議室預約詳情
def appointment(request, id):
    room = get_object_or_404(ConfeRoom, id=id)
    d = datetime.date.today()
    order = Order.objects.filter(room=room, start_time__gte=d).order_by('start_time')
    content = {
        'order': order,
        'room': room
    }
    return render(request, 'order.html', content)

def logi(request):
    form = Logi_form()
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        u = authenticate(username=username, password=password)
        if u and u.is_active:
            login(request, u)
            return redirect('dinosaur:list')

    content = {
        'form': form
    }
    return render(request, 'logi.html', content)

def logo(request):
    if request.user.is_active:
        logout(request)
        return redirect('dinosaur:list')

def register(request):
    form = Register_form(request.POST)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user.username = username
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user.is_active:
            login(request, user)
            return redirect('dinosaur:list')

    content = {
        'form': form
    }
    return render(request, 'logi.html', content)

def add(request, id):
    if not request.user.is_active:
        return redirect('dinosaur:register')

    form = Add_form(request.POST)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.room = ConfeRoom.objects.get(id=id)
        order_list = Order.objects.filter(room=instance.room)
        start_time_list = [order.start_time for order in order_list]

        # 手动设置开始时间
        iso_formatted_date = request.POST['time']
        instance.start_time = parser.isoparse(iso_formatted_date)
        instance.start_time = timezone.make_aware(instance.start_time)  # 将时间设置为时区感知的

        if instance.start_time not in start_time_list:
            if date_is_valid(instance.start_time, instance.room):  # 传递房间参数
                instance.end_time = instance.start_time + timedelta(hours=1)
                instance.save()
                return redirect('/meeting/%s' % id)
            else:
                messages.error(request, '超出預約範圍')
                return redirect('/meeting/%s' % id)
        else:
            messages.error(request, '已被預約')
            return redirect('/meeting/%s' % id)

    context = {
        "form": form,
    }
    return render(request, 'logi.html', context)



def delete(request, room_id, order_id):
    order = get_object_or_404(Order,id=order_id)
    if order.user != request.user:
        raise Http404
    order.delete()
    messages.success(request,'删除成功！')
    return redirect('/meeting/%s' % room_id)


#設置預約範圍，判斷是否合法

def date_is_valid(start_date, room):
    # 获取当前时间
    current_time = timezone.now()

    # 检查开始日期是否不是 None 并且在未来
    if start_date is not None and start_date > current_time:
        # 获取1小时后的时间
        end_date = start_date + timedelta(hours=1)

        # 检查是否与现有预约时间冲突
        existing_orders = Order.objects.filter(room=room, start_time__lt=end_date, end_time__gt=start_date)
        if not existing_orders.exists():
            return True  # 未与现有预约冲突，可以预约

    # 如果日期为 None、在过去或与现有预约冲突，返回 False
    return False

def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('calendar')  # 重定向回月历页面
    else:
        form = EventForm()
    
    return render(request, 'create_event.html', {'form': form})


def compact_calendar(request):
     return render(request, 'calendar.html', {'calendar': compact_calendar()})

def calendar_view(request):
    # 查询数据库获取会议室预约信息
    reservations = Order.objects.all()
    
    # 创建一个包含预约信息的字典，显示开始时间
    events = [{'title': str(reservation.user), 'start': reservation.start_time, 'end': reservation.end_time} for reservation in reservations]
    
    context = {
        'events': events,
    }
    
    return render(request, 'calendar.html', context)

def calendar_data(request):
    # 查询数据库获取会议室预约信息
    reservations = Order.objects.all()

    # 创建一个包含预约信息的列表，1小时一个时段
    events = []
    for reservation in reservations:
        start_time = reservation.start_time
        end_time = reservation.end_time

        while start_time < end_time:
            event = {
                'title': str(reservation.user),
                'start': start_time.isoformat(),
                'end': (start_time + timedelta(hours=1)).isoformat()
            }
            events.append(event)
            start_time += timedelta(hours=1)

    return JsonResponse(events, safe=False)

