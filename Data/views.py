# -*- encoding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from Data.models import *
from datetime import datetime
import time
# Create your views here.

def index(request):
    return render(request,'index.html')

def guide(request):
    return render(request,'guide.html')

def home(request):
    return render(request,'home.html')

def admin(request):
    return render(request,'admin.html')

def help(request):
    return render(request,'help.html')

def send(request):	
	basin = Basin.objects.all()
	data = {
		'basin':basin,
    }
	return render(request, 'send.html', data)  

def list_pay(request):
    head_table = ["Reservorio","Fecha","Nivel Cloro (ppm)","Cloración","Caudal (l/s)","Usu. Pagantes"]
    measurement = Measurement.objects.values('reservoir_id','date','level_cl','add_cl','caudal','user_pay')
    basin = Basin.objects.all()
    reservoir = Reservoir.objects.all()

    data = {
        'measurement': measurement,
        'head_table':head_table,
        'reservoir':reservoir
    }
    return render(request, 'list_pay.html', data)

def new_message(request):
    head_table = ["Reservorio","Fecha","Hora","Mensaje"]
    record = Record.objects.filter(process=False).values('reservoir_id','date','time','message')
    
    data = {
        'head_table':head_table,
        'record':record
    }
    return render(request, 'new_message.html', data)

def login(request):
    return render(request,'login.html')

def search_reservoir(request):    
    if request.method == 'GET':
    	basin_id = request.GET["basin_id"]
    	basin = Basin.objects.all()
    	reservoir = list(Reservoir.objects.filter(basin_id=str(basin_id)).values('reservoir_id','manager_id'))
    else:
        basin = Basin.objects.all()
        reservoir = Reservoir.objects.all()
    return JsonResponse(reservoir,safe=False)

def search_measurement_graf(request):
    if request.method == 'GET':
        date_end = time.strftime("%Y-%m-%d")
        date_start = BackDate(date_end,3)

        basin_id = request.GET["basin_id"]
        
        list_reservoir = Reservoir.objects.filter(basin_id=str(basin_id)).values('reservoir_id',)
        l = []
        for k in range(len(list_reservoir)):
            l.append(list_reservoir[k]["reservoir_id"])
        measurement = list(Measurement.objects.filter(reservoir_id__in=l,date__range=[date_start, date_end]).values('reservoir_id','date','time',
            'level_cl','add_cl','caudal','user_pay').order_by('reservoir_id','date'))
    else:
        measurement = Measurement.objects.all()

    result = []
    reser = ['Fecha']
    for k in range(len(measurement)):
        aux = measurement[k]['reservoir_id']
        if aux not in reser:
            reser.append(aux)
    result.append(reser)
    try:
        f = int(len(measurement)/(len(reser)-1))
    except Exception as e:
        f = 0    
    # print(str(f))
    for i in range(f):
        ll = [str(measurement[i]['date'])[0:7]]
        for j in range(i,len(measurement),f):
            n1 = float(measurement[j]['user_pay'].split('/')[0])
            n2 = float(measurement[j]['user_pay'].split('/')[1])
            aux = round(n1/n2*100)
            ll.append(aux)
        result.append(ll)
    # print(result)
    return JsonResponse(result,safe=False)

def search_measurement(request):
    if request.method == 'GET':        
        reservoir_id = request.GET["reservoir_id"]
        date_id = str(request.GET["date"]).split(' ')
        
        date = date_id[1]+'-'+date_id[0]+'-20'
        print(date)
        date_end = date
        date_start = BackDate(date,0)
               
        measurement = list(Measurement.objects.filter(reservoir_id=reservoir_id,date__range=[date_start, date_end]).values('reservoir_id','date',
            'level_cl','add_cl','caudal','user_pay').order_by('reservoir_id','date'))
    else:
        measurement = Measurement.objects.all()
    
    return JsonResponse(measurement,safe=False)

def map(request):
    date_end = time.strftime("%Y-%m-%d")
    date_start = BackDate(date_end,0)
    reservoir = list(Reservoir.objects.all().order_by('reservoir_id'))

    measurement = list(Measurement.objects.filter(date__range=[date_start, date_end]).values('reservoir_id','time',).order_by('reservoir_id'))
    data = {
		'reservoir':reservoir,
        'measurement':measurement
    }
    return render(request, 'map.html', data)

def send_msg(request):	
	if request.method == 'GET':
		managers_phone = request.GET["managers_phone"]
		msg = request.GET["msg"]

		time_ = time.strftime("%H:%M:%S")
		date_ = time.strftime("%Y-%m-%d")

		list_manager_phone = managers_phone.split(",")
		for k in range(len(list_manager_phone)):
			phone = list_manager_phone[k]
			box = Outbox(outbox_id=phone,message=msg,date=date_,time=time_)
			box.save()
		res = "Envio Exitoso"
	else:
	    res = "Error"	
	return HttpResponse(res)

def pie(request):   
    basin = list(Basin.objects.all())
    basin_l = list(Basin.objects.all())
    data = {
        'basin':basin,
    }
    return render(request, 'pie.html', data)    

def BackDate(dates,f):
    date_ = str(dates).split('-') #time.strftime("%Y-%m-%d").split('-')
    d = int(date_[2])
    m = int(date_[1])
    y = int(date_[0])
    x = m-f

    if x <= 0:
        D =1
        M = 12+x
        Y = y-1
    else:
        D =1
        M = x
        Y = y
    return str(Y)+"-"+str(M)+"-"+str(D)

