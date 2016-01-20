'''
Created on 9 Nov 2015

@author: Chakmi
'''
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import Http404
from django.http.response import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView

from mysite import settings
from mysite.forms import RegistrationForm, UserForm
from restoran.forms import MapForm
from restoran.models import Korisnik, Poseta


@csrf_exempt
def index(request):
    if request.user.is_authenticated():
        pozvan = []
        korisnik = Korisnik.objects.get(user__pk=request.user.pk)
        
        posete_sve = Poseta.objects.all()
        for poseta in posete_sve:
            for zvanica in poseta.zvanice.all():
                if zvanica.korisnik.pk == korisnik.pk:
                    if zvanica.stanje == 'A':
                        pozvan.append(poseta)
        
        ppozvan = []
            
        #gleam da li je ulogovani korisnik u restoranima gde je pozvan da li je dao ocenu
        for poseta in pozvan:
            for zvanica in poseta.zvanice.all():
                if zvanica.korisnik.pk == korisnik.pk:
                    ppozvan.append((poseta, zvanica.ocena))
        
        posete = Poseta.objects.all().filter(rezervacija__korisnik__pk = korisnik.pk)
        context = {'user': korisnik, 'posete':posete, 'pozvan':ppozvan}
        return render(request, 'restoran/home.html', context)
    
    username = request.POST.get('username', "")
    password = request.POST.get('password', "")
    
    user = auth.authenticate(username=username, password=password)
    
    if user:
        if user.is_active:
            auth.login(request, user)
            
            pozvan = []
            korisnik = Korisnik.objects.get(user__pk=request.user.pk)
            
            posete_sve = Poseta.objects.all()
            for poseta in posete_sve:
                for zvanica in poseta.zvanice.all():
                    if zvanica.korisnik.pk == korisnik.pk:
                        if zvanica.stanje == 'A':
                            pozvan.append(poseta)
            
            ppozvan = []
            
            #gleam da li je ulogovani korisnik u restoranima gde je pozvan da li je dao ocenu
            for poseta in pozvan:
                for zvanica in poseta.zvanice.all():
                    if zvanica.korisnik.pk == korisnik.pk:
                        ppozvan.append((poseta, zvanica.ocena))
            
            posete = Poseta.objects.all().filter(rezervacija__korisnik__pk = korisnik.pk)
            context = {'user': korisnik, 'posete':posete, 'pozvan':ppozvan}
            return render(request, 'restoran/home.html', context)
        else:
            context = {'invalid': 'Username and/or password are not correct or profile is not active'}
            return render(request, 'restoran/index.html', context)
        
    context = {'invalid': ''}
    return render(request, 'restoran/index.html', context)

def logout(request):
    auth.logout(request)
    context = {'invalid': ''}
    return render(request, 'restoran/index.html', context)

def aktiviraj(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.is_active = True
    user.save()
    
    #create user and korisnik
    korisnik = Korisnik(user=user)
    korisnik.save()
    korisnik.prijatelji = []
    
    context = {'invalid': 'Profile is active'}
    return render(request, 'restoran/index.html', context)

class UserCreate(CreateView):
    model = Korisnik
    template_name = 'restoran/register.html'
    form_class = RegistrationForm
    
    def get_success_url(self):
        return reverse('home')
    
    def form_valid(self, form):
        form.instance.is_active = False
        response = super(UserCreate, self).form_valid(form)
        
        link = reverse('aktiviraj', args={self.object.id})
        adresa = self.request.META['HTTP_HOST']+link
        
        send_mail('Account activation ', 'Activate your account on RestauranTrac with this link  http://'+adresa, settings.EMAIL_HOST_USER,[form.instance.email])
        
        return response
    
    def get_context_data(self, **kwargs):
        context = super(UserCreate, self).get_context_data(**kwargs)
        
        #KeyError
        try:
            context["back"] = self.request.META["HTTP_REFERER"]
        except(KeyError):
            context["back"]="/"
     
        return context

def sort_list(cmd, korisnik):
    if cmd == 'ascName':
        return korisnik.prijatelji.order_by("user__first_name")
    elif cmd=='descName':  
        return korisnik.prijatelji.order_by("-user__first_name")
    elif cmd=='ascTip':
        return korisnik.prijatelji.order_by("user__last_name")
    elif cmd=='descTip':
        return korisnik.prijatelji.order_by("-user__last_name")
    else:
        return korisnik.prijatelji.all()
    
class ProfilDetail(DetailView):
    model = Korisnik
    template_name = 'restoran/profil.html'
    context_object_name = 'korisnik'
    
    '''def get_object(self):
        try:
            user = User.objects.get(pk = self.request.user.pk)
            return Korisnik.objects.get(user__pk=user.pk)
        except ObjectDoesNotExist:
            return redirect(reverse('home'))
        
        #user = get_object_or_404(User, pk=self.request.user.pk)'''
        
    
    def get(self, request, **kwargs):
        try:
            user = User.objects.get(pk = self.request.user.pk)
            self.model.objects.get(pk=Korisnik.objects.get(user__pk=user.pk).pk)
            return Korisnik.objects.get(user__pk=user.pk).pk
        except ObjectDoesNotExist:
            return redirect(reverse('home'))
    
    def get_context_data(self, **kwargs):
        context = super(ProfilDetail, self).get_context_data(**kwargs)
        
        user = get_object_or_404(User, pk=self.request.user.pk)
        korisnik = Korisnik.objects.get(user__pk=user.pk)
        
        poseta = []
        pos =  Poseta.objects.all().filter(zvanice__korisnik__pk=korisnik.pk)
        
        for p in pos:
            for z in p.zvanice.all():
                if z.korisnik.pk == korisnik.pk:
                    poseta.append((p, z.stanje))
        
        context['poseta'] = poseta
        
        try:
            value = self.request.GET['sort_by']
            context["prijatelji"] = sort_list(value, korisnik)
        except MultiValueDictKeyError:
            context["prijatelji"] = korisnik.prijatelji.all()
        
        #KeyError
        try:
            context["back"] = self.request.META["HTTP_REFERER"]
        except(KeyError):
            context["back"]="/"
     
        return context
    
class UpdateProfil(UpdateView):
    model = User
    template_name = 'restoran/profileupdate.html'
    form_class = UserForm
    
    def get_success_url(self):
        return reverse('profil')
    
    
    def get_context_data(self, **kwargs):
        context = super(UpdateProfil, self).get_context_data(**kwargs)
        
        #KeyError
        try:
            context["back"] = self.request.META["HTTP_REFERER"]
        except(KeyError):
            context["back"]="/"
     
        return context
    
def myprifl(request):
    if request.user.is_authenticated():
        context = {}
        user = get_object_or_404(User, pk=request.user.pk)
        korisnik = Korisnik.objects.get(user__pk=user.pk)
        
        poseta = []
        pos =  Poseta.objects.all().filter(zvanice__korisnik__pk=korisnik.pk)
        
        for p in pos:
            for z in p.zvanice.all():
                if z.korisnik.pk == korisnik.pk:
                    poseta.append((p, z.stanje))
        
        context['poseta'] = poseta
        
        try:
            value = request.GET['sort_by']
            context["prijatelji"] = sort_list(value, korisnik)
        except MultiValueDictKeyError:
            context["prijatelji"] = korisnik.prijatelji.all()
        
        #KeyError
        try:
            context["back"] = request.META["HTTP_REFERER"]
        except(KeyError):
            context["back"]="/"
        
        context['korisnik'] = korisnik
        
        return render(request, 'restoran/profil.html', context)
    
    context = {'invalid': 'Username and/or password are not correct or profile is not active'}
    return render(request, 'restoran/index.html', context)
    