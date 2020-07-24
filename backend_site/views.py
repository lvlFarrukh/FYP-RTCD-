from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.contrib.sessions.models import Session
from django.shortcuts import HttpResponse
from django.core.files.storage import FileSystemStorage


def index(request):
    if request.session.has_key('login_id'):
        data = controller_user.objects.get(id=request.session['login_id'])
        count1 = len(suspect_person_detail.objects.all())
        # print(count1)
        data.name = data.name.split(" ")[0]
        return render(request, 'backend_site/index.html', {'data': data, 'front_count':[count1]})
    else:
        return redirect('login')

def login(request):
    if request.session.has_key('login_id'):
        return redirect('index')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            auth = controller_user.objects.get(email=email, password=password)
            # print(auth.id,"`````````````````````````")
            if auth:
                request.session['login_id'] = auth.id

                return redirect('index')
        except:
            return render(request, 'backend_site/login.html')
    return render(request, 'backend_site/login.html')

def logout(request):
    del request.session['login_id']
    return redirect('login')


def add_suspect(request):

    if request.session.has_key('login_id'):
        data = controller_user.objects.get(id=request.session['login_id'])
        data.name = data.name.split(" ")[0]
        return render(request, 'backend_site/add_suspect.html', {'data': data})
    else:
        return redirect('login')


def add_suspect_data(request):

    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        gender = request.POST.get('gender')
        cnic = request.POST.get('cnic')
        address = request.POST.get('address')
        education = request.POST.get('education')
        marital_status = request.POST.get('marital_status')
        age = request.POST.get('age')
        date_of_birth = request.POST.get('date_of_birth')
        nationality = request.POST.get('nationality')

        insert_data = suspect_person_detail(first_name=first_name, last_name=last_name,
                                            gender=gender, cnic=cnic, address=address,
                                            education=education, marital_status=marital_status,
                                            age=age, date_of_birth=date_of_birth, nationalilty=nationality)

        insert_data.save()

        fs = FileSystemStorage()

        for i in request.FILES:
            request.FILES[i].name = f"{insert_data.id}_user.{(request.FILES[i].name).split('.')[1]}"
            fs.save(request.FILES[i].name, request.FILES[i])
            # print(request.FILES[i].size)
        return redirect('add_suspect')

    else:
        return redirect('Add_suspect')



def user(request):
    if request.session.has_key('login_id'):
        data = controller_user.objects.get(id=request.session['login_id'])
        data.name = data.name.split(" ")[0]
        return render(request, 'backend_site/user.html', {'data': data})
    else:
        return redirect('login')


def suspect_list(request):
    if request.session.has_key('login_id'):
        data = controller_user.objects.get(id=request.session['login_id'])
        suspect_data = suspect_person_detail.objects.all()
        # print(data)
        return render(request, 'backend_site/suspects_list.html', {'suspect_data': suspect_data,
                                                                   'data': data, 'length':len(suspect_data)})
    else:
        return redirect('login')


def identify_suspects(request):
    if request.session.has_key('login_id'):
        data = controller_user.objects.get(id=request.session['login_id'])
        identify_suspect = suspect_person_detail.objects.get(status=True)
        # print(identify_suspect,'``````````````')
        try:
            return render(request, 'backend_site/suspects_list.html', {'identify_suspect': identify_suspect,
                                                                       'data': data, 'length':len(identify_suspect)})
        except:
            # print(identify_suspect.first_name)
            return render(request, 'backend_site/identify_suspects.html', {'identify_suspect': identify_suspect,
                                                                       'data': data, 'length': 0})
    else:
        return redirect('login')