from django.shortcuts import render, reverse
from django.http.response import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.template.context_processors import request
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .models import Document, Animal
from MySQLdb.compat import long
from django.contrib.sites import requests
from .orb import *
from .fmatch import *

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
        if(request.POST.get('type', None) == 'logout'):
            logout(request)
            return JsonResponse({'data': 'logout'})
        elif(request.POST.get('checker', '') != ''):
            return HttpResponseRedirect(reverse("botchat:authPage"))
        elif(request.POST.get('imageSearch', '') != ''):
            
            images_path = '../media/animals/'
            files = []
            for p in Animal.objects.all():
                files.append(p.image)
            print(files)
#             files = [os.path.join(images_path, p) for p in sorted(os.listdir(images_path))]
            # getting 3 random images 
            # sample = random.sample(files, 5)
            sample = files
            batch_extractor(images_path)
            
# 
            ma = Matcher('features.pck')
# 
            s = request.FILES['image']
            
            for s in sample:
                names, match = ma.match(s, topn=5)
    #        
                for i in range(5):
#             # we got cosine distance, less cosine distance between vectors
#             # more they similar, thus we subtruct it from 1 to get match value
                    print(names[i])
                    print ('Match %s' % (1-match[i]))
#             show_img(os.path.join(images_path, names[i]))

        elif(request.FILES['files']):
            file = request.FILES['files']
            longitude = request.POST.get('longitude', -1)
            latitude = request.POST.get('latitude', -1)   
            if(longitude == ""):
                longitude = -1
                latitude = -1
            doc = Document.objects.create(document = file, longitude = float(longitude), latitude = float(latitude))
            doc.save()
            return HttpResponseRedirect(reverse("botchat:authPage"))
        return HttpResponseRedirect(reverse("botchat:authPage"))
    

class api(generic.ListView):
    
    def get(self, request):
        s = request.GET.get('id', None)
        p = request.GET.get('p', None)
        print(s, p)
        return JsonResponse({'data': "Hello"})

    def post(self, request):
        print("AYA", request.POST.get('message', None))
        return JsonResponse({'data': "Hello"})