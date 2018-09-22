from django.shortcuts import render, reverse
from django.http.response import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.template.context_processors import request


class IndexView(generic.ListView):
    
    template_name = 'botchat/home.html'

    def get(self, request):
        user = request.user
        if(not user.is_anonymous):
            return  HttpResponseRedirect(reverse('botchat:authPage'))
        return render(request, self.template_name)
    
class HomeView(generic.ListView):
    
    template_name = 'botchat/mainPage.html'

    def get(self, request):
        user = request.user
        if(not user.is_anonymous):
            return  render(request, self.template_name)
        return HttpResponseRedirect(reverse('botchat:home'))

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

class api(generic.ListView):
    
    def get(self, request):
        s = request.GET.get('id', None)
        p = request.GET.get('p', None)
        print(s, p)
        return JsonResponse({'data': "Hello"})

    def post(self, request):
        print("AYA", request.POST.get('message', None))
        return JsonResponse({'data': "Hello"})