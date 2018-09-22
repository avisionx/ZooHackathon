from django.shortcuts import render, reverse
from django.http.response import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.template.context_processors import request
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .models import Document
from MySQLdb.compat import long

class IndexView(generic.ListView):
    
    template_name = 'botchat/home.html'

    def get(self, request):
        user = request.user
        if(not user.is_anonymous):
            return  HttpResponseRedirect(reverse('botchat:authPage'))
        return render(request, self.template_name)
    
    def post(self, request):
        if(request.POST.get('type', None) == 'log'):
            username = request.POST.get('username', None)
            password = request.POST.get('password', None)
            if(User.objects.filter(username=username).exists()):
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return JsonResponse({'data': "success"})
        elif(request.POST.get('type', None) == 'sign'):
            firstName = request.POST.get('firstName', None)
            lastName = request.POST.get('lastName', None)
            email = request.POST.get('email', None)
            username = request.POST.get('username', None)
            password = request.POST.get('password', None)
            if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
                User.objects.create_user(username, email, password)
                user = authenticate(username = username, password = password)
                login(request, user)
                return JsonResponse({'data': "success"})
        return JsonResponse({'data': "failure"})
    
class HomeView(generic.ListView):
    
    template_name = 'botchat/mainPage.html'

    def get(self, request):
        user = request.user
        if(not user.is_anonymous):
            return  render(request, self.template_name)
        return HttpResponseRedirect(reverse('botchat:home'))
    
    def post(self, request):
        print(request.POST)
        if(request.POST.get('type', None) == 'logout'):
            logout(request)
            return JsonResponse({'data': 'logout'})
        elif(request.POST.get('type', None) == 'uploadData'):
            file = request.POST.get('files', None)
            if(file != ''):
                longitude = request.POST.get('longitude', -1)
                latitude = request.POST.get('latitude', -1)
                print(longitude, latitude)
                if(longitude != -1):
                    doc = Document.objects.create(document = file, longitude = longitude, latitude = latitude)
                    doc.save()   
                    return JsonResponse({'data': 'successUpload'})
                else:
                    JsonResponse({'data': 'reset'})
            else:
                JsonResponse({'data': 'reset'})
        return JsonResponse({'data': 'working'})
    

class api(generic.ListView):
    
    def get(self, request):
        s = request.GET.get('id', None)
        p = request.GET.get('p', None)
        print(s, p)
        return JsonResponse({'data': "Hello"})

    def post(self, request):
        print("AYA", request.POST.get('message', None))
        return JsonResponse({'data': "Hello"})