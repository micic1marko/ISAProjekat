import datetime
import json

from django.contrib import auth
from django.contrib.auth.decorators import user_passes_test
from django.contrib.gis.geoip2 import GeoIP2  # @UnusedImport
from django.core.mail import send_mail
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Q
from django.http.response import HttpResponse  # @UnusedImport
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from gmapi import maps

from mysite import settings
from restoran.forms import SearchFriendsForm, AddFriendsForm, RezervacijaForm, \
    OceniForm, MapForm, JeloUpdateForm, ImageUploadForm
from restoran.models import Restoran, Jelo, Korisnik, VrstaRestorana, \
    Rezervacija, Poseta, Pozivnica, Ocena, Sto


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
                        print poseta.pk
                        ppozvan.append((poseta, zvanica.ocena))
            
            posete = Poseta.objects.all().filter(rezervacija__korisnik__pk = korisnik.pk)
            context = {'user': korisnik, 'posete':posete, 'pozvan':ppozvan}
            return render(request, 'restoran/home.html', context)
        else:
            context = {'invalid': 'Username and/or password are not correct or profile is not active'}
            return render(request, 'restoran/index.html', context)
        
    context = {'invalid': ''}
    return render(request, 'restoran/index.html', context)

def izmenarestorana(request, pk):
    
    korisnik = Korisnik.objects.get(user__pk=request.user.pk)
    restoran = get_object_or_404(Restoran, pk=pk)
    
    context = {'user': korisnik, 'restoran': restoran}
    return render(request, 'restoran/izmenarestorana.html', context)

def searchfriends(request):
    if request.method == 'POST':
        form = SearchFriendsForm(request.POST)
        
        if form.is_valid():
            text = form.cleaned_data['text'].split(" ")
            user = request.user
            korisnik = Korisnik.objects.get(user__pk=user.pk)
            
            full_rez = []
            
            for t in text:
                rez = Korisnik.objects.filter(Q(user__first_name__icontains=t) | Q(user__last_name__icontains=t) | 
                                              Q(user__username__icontains=t)).exclude(Q(pk=korisnik.pk) | Q(user__is_staff=True))
                                              
                for rr in [r for r in rez if r not in full_rez]:
                    full_rez.append(rr)
            
        
            return render(request, 'restoran/searchfriends.html', {'result': full_rez, 'user': korisnik})

def dodajprijatelja(request):
    if request.method == 'POST':
        form = AddFriendsForm(request.POST)
        
        if form.is_valid():
            user_pk = form.cleaned_data['user_pk']#Korisnik
            friend_pk = form.cleaned_data['friend_pk']
            
            korisnik = Korisnik.objects.get(pk=user_pk)
            friend = Korisnik.objects.get(pk=friend_pk)#Korisnik
            
            
            korisnik.prijatelji.add(friend)
            friend.prijatelji.add(korisnik)
            
            return render(request, 'restoran/prijatelji.html', {'user': korisnik, 'prijatelji':korisnik.prijatelji.all()})

def sort_friend_list(cmd, korisnik):
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

def prijatelji(request):
    user = request.user
    korisnik = Korisnik.objects.get(user__pk=user.pk)
    
    context = {'user': korisnik}
    
    try:
        value = request.GET['sort_by']
        context['prijatelji'] = sort_friend_list(value, korisnik)
    except MultiValueDictKeyError:
        context['prijatelji'] = korisnik.prijatelji.all()
    
    '''if request.user != korisnik.user:
        return HttpResponse('Nemate pravo pristupa')'''
    
    return render(request, 'restoran/prijatelji.html', context)

def unfriend(request, pk):
    user = request.user
    korisnik = Korisnik.objects.get(user__pk = user.pk)
    
    friend = Korisnik.objects.get(pk=pk)
    korisnik.prijatelji.remove(friend)
    
    return render(request, 'restoran/profil.html', {'korisnik': korisnik})

def oceni(request, pk):
    if request.method == 'POST':
        form = OceniForm(request.POST)
        
        user = request.user
        korisnik = Korisnik.objects.get(user__pk = user.pk)
        
        if form.is_valid():
            ocena = form.cleaned_data['ocena']
            
            poseta = get_object_or_404(Poseta, pk=pk)
            poseta.ocena = ocena
            poseta.save()
            
            restoran = poseta.rezervacija.restoran
            
            ocena_new = Ocena(ocena=ocena, ocenjivac=korisnik)
            ocena_new.save()
            
            restoran.ocene.add(ocena_new)
            
    pozvan = []
    korisnik = Korisnik.objects.get(user__pk=request.user.pk)
    
    posete_sve = Poseta.objects.all()
    for poseta in posete_sve:
        for zvanica in poseta.zvanice.all():
            if zvanica.korisnik.pk == korisnik.pk:
                if zvanica.stanje == 'A':
                    pozvan.append(poseta)
    
    
    posete = Poseta.objects.all().filter(rezervacija__korisnik__pk = korisnik.pk)
    context = {'user': korisnik, 'posete':posete, 'pozvan':pozvan}
    return render(request, 'restoran/home.html', context)

def prihvati(request, pk):
    user = request.user
    poseta = get_object_or_404(Poseta, pk=pk)
    
    korisnik = Korisnik.objects.get(user__pk=user.pk)
    
    for z in poseta.zvanice.all():
        if z.korisnik.pk == korisnik.pk:
            z.stanje = 'A'
            z.save()
            
    pozvan = []
        
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
                
    #return render(request, 'restoran/profil.html', {'korisnik': user})

def odustani(request, pk):
    user = request.user
    poseta = get_object_or_404(Poseta, pk=pk)
    
    korisnik = Korisnik.objects.get(user__pk=user.pk)
    
    for z in poseta.zvanice.all():
        if z.korisnik.pk == korisnik.pk:
            z.stanje = 'D'
            z.save()
    
        pozvan = []
        
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
                
    #return render(request, 'restoran/profil.html', {'korisnik': user})

def ocenipoziv(request, pk):
    if request.method == 'POST':
        form = OceniForm(request.POST)
        
        user = request.user
        korisnik = Korisnik.objects.get(user__pk = user.pk)
        
        if form.is_valid():
            ocena = form.cleaned_data['ocena']
            
            poseta = get_object_or_404(Poseta, pk=pk)
            poseta.ocena = ocena
            poseta.save()
            
            #Ocenjivanje restorana iz posete
            restoran = poseta.rezervacija.restoran
            
            ocena_new = Ocena(ocena=ocena, ocenjivac=korisnik)
            ocena_new.save()
            
            restoran.ocene.add(ocena_new)
            
            #Ocenjivanje restorana za poziv
            for poziv in poseta.zvanice.all():
                if poziv.korisnik.pk == korisnik.pk:
                    poziv.ocena = ocena
                    poziv.save()
                    break
    
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
    
    
    posete = Poseta.objects.all().filter(rezervacija__korisnik__pk = korisnik.pk)
    context = {'user': korisnik, 'posete':posete, 'pozvan':ppozvan}
    return render(request, 'restoran/home.html', context)

def sort_list(cmd):
    if cmd == 'ascName':
        return Restoran.objects.order_by("naziv")
    elif cmd=='descName':  
        return Restoran.objects.order_by("-naziv")
    elif cmd=='ascTip':
        return Restoran.objects.order_by("-tip")
    elif cmd=='descTip':
        return Restoran.objects.order_by("tip")
    else:
        return Restoran.objects.all()
        

class RestoraniList(ListView):
    model = Restoran
    template_name = 'restoran/restorani.html'
    context_object_name = 'obj'
    
    def get_queryset(self):
        korisnik = Korisnik.objects.get(user__pk = self.request.user.pk)
        if korisnik.user.is_staff:
            return Restoran.objects.all().filter(menadzer__pk=korisnik.pk)
        else:
            try:
                value = self.request.GET['sort_by']
                return sort_list(value)
            except MultiValueDictKeyError:
                return Restoran.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super(RestoraniList, self).get_context_data(**kwargs)
        
        korisnik = Korisnik.objects.get(user__pk = self.request.user.pk)
        '''
        user je DJANGO user tabela
        korinik je KORISNIK tabela koju smo definisali
        i koja je 1-1 vezana sa USER tabelom koja je DJANGOVA :D
        '''
        
        context["user"] = korisnik
        #KeyError
        try:
            context["back"] = self.request.META["HTTP_REFERER"]
        except(KeyError):
            context["back"]="/"
            
        return context
    
class RestoranDetail(DetailView):
    model = Restoran
    template_name = 'restoran/restoran.html'
    context_object_name = 'restoran'
    
    def get_context_data(self, **kwargs):
        context = super(RestoranDetail, self).get_context_data(**kwargs)
        
        pk = self.kwargs['pk']
        restoran = get_object_or_404(Restoran, pk=pk)
        
        gmap = maps.Map(opts = {
        'center': maps.LatLng(restoran.lat, restoran.lon),
        'mapTypeId': maps.MapTypeId.ROADMAP,  # @UndefinedVariable
        'zoom': 3,
        'mapTypeControlOptions': {
             'style': maps.MapTypeControlStyle.DROPDOWN_MENU  # @UndefinedVariable
        },
        })
        
        marker = maps.Marker(opts = {
            'map': gmap,
            'position': maps.LatLng(restoran.lat, restoran.lon),
        })
        maps.event.addListener(marker, 'mouseover', 'myobj.markerOver')
        maps.event.addListener(marker, 'mouseout', 'myobj.markerOut')
        info = maps.InfoWindow({
            'content': restoran.naziv,
            'disableAutoPan': True
        })
        info.open(gmap, marker)
        
        korisnik = Korisnik.objects.get(user__pk = self.request.user.pk)
        
        context["user"] = korisnik
        context["form"] = MapForm(initial={'map': gmap})
        
        #prosecna ocena
        value = 0
        for o in restoran.ocene.all():
            value = value + o.ocena
            
        count = restoran.ocene.all().count()
        context['rate'] = '%.1f' % round(float(value)/float(count), 1)
        
        #prosecna ocena prijatelja
        new_rate = 0;
        i = 0
        
        for ocena in restoran.ocene.all():
            if ocena.ocenjivac.pk == korisnik.pk:
                new_rate = new_rate + ocena.ocena
                i = i+1
            elif ocena.ocenjivac in korisnik.prijatelji.all():
                new_rate = new_rate + ocena.ocena
                i = i+1
        
        context['friend_rate'] = '%.1f' % round(float(new_rate)/float(i), 1)
        
        #KeyError
        try:
            context["back"] = self.request.META["HTTP_REFERER"]
        except(KeyError):
            context["back"]="/"
            
        return context
    
class JeloDetail(DetailView):
    model = Jelo
    template_name = 'restoran/jelo.html'
    context_object_name = 'jlvk'
    
    def get_context_data(self, **kwargs):
        context = super(JeloDetail, self).get_context_data(**kwargs)
        korisnik = Korisnik.objects.get(user__pk = self.request.user.pk)
        
        context["user"] = korisnik
        
        return context

class JeloUpdate(UpdateView):
    model = Jelo
    form_class = JeloUpdateForm
    template_name = 'restoran/updatejelo.html'
    
    def get_success_url(self):
        return reverse('izmenarestorana', args={self.get_object().id, })
    
    def get_context_data(self, **kwargs):
        context = super(JeloUpdate, self).get_context_data(**kwargs)
        korisnik = Korisnik.objects.get(user__pk = self.request.user.pk)
        
        context["user"] = korisnik
        
        return context
    
class JeloDelete(DeleteView):
    model = Jelo
    template_name = 'restoran/deletejelo.html'
    
    def get_success_url(self):
        return reverse('izmenarestorana', args={self.get_object().id, })
    
    def get_context_data(self, **kwargs):
        context = super(JeloDelete, self).get_context_data(**kwargs)
        korisnik = Korisnik.objects.get(user__pk = self.request.user.pk)
        
        context["user"] = korisnik
        
        return context
    
class JeloCreate(CreateView):
    model = Jelo
    template_name = 'restoran/createjelo.html'
    form_class = JeloUpdateForm
    
    def get_success_url(self):
        return reverse('izmenarestorana', args={self.kwargs['pk'], })
    
    def form_valid(self, form):
        restoran = get_object_or_404(Restoran, pk=self.kwargs['pk'])
        response = super(JeloCreate, self).form_valid(form)
        
        restoran.jelovnik.add(form.instance)
        
        return response
    
    def get_context_data(self, **kwargs):
        context = super(JeloCreate, self).get_context_data(**kwargs)
        korisnik = Korisnik.objects.get(user__pk = self.request.user.pk)
        
        context["user"] = korisnik
        
        return context
    
class TipRestoranaDetail(DetailView):
    model = VrstaRestorana
    template_name = 'restoran/tiprestorana.html'
    context_object_name = 'tiprestorana'
    
    def get_context_data(self, **kwargs):
        context = super(TipRestoranaDetail, self).get_context_data(**kwargs)
        korisnik = Korisnik.objects.get(user__pk = self.request.user.pk)
        
        context["user"] = korisnik
        
        return context

class CreateRezervacija(CreateView):
    model = Rezervacija
    template_name = 'restoran/rezervacija.html'
    form_class = RezervacijaForm
    
    def get_success_url(self):
        return reverse('home')
    
    def get_context_data(self, **kwargs):
        context = super(CreateRezervacija, self).get_context_data(**kwargs)
        restoran = get_object_or_404(Restoran, pk=self.kwargs['pk'])
        korisnik = Korisnik.objects.get(user__pk = self.request.user.pk)
        
        context["user"] = korisnik
        
        context["restoran_pk"] = restoran.pk
        
        return context
    
    def get_form(self, form_class):
        form = super(CreateRezervacija,self).get_form(form_class) #instantiate using parent
        new_user = Korisnik.objects.get(user__pk = self.request.user.pk)
        form.fields['zvanice'].queryset = new_user.prijatelji
        
        restoran = get_object_or_404(Restoran, pk=self.kwargs['pk'])
        form.fields['stolovi'].queryset = restoran.stolovi

        return form
    
    def form_valid(self, form):
        korisnik = Korisnik.objects.get(user__pk =self.request.user.pk)
        form.instance.korisnik = korisnik
        
        restoran = get_object_or_404(Restoran, pk=self.kwargs['pk'])
        form.instance.restoran = restoran
        
        response = super(CreateRezervacija, self).form_valid(form)
        
        for sto in form.instance.stolovi.all():
            sto.stanje = 'R'
            sto.save()
        
        posetioci = form.instance.zvanice.all()
        
        rez = get_object_or_404(Rezervacija, pk= form.instance.pk)
        poseta = Poseta(rezervacija=rez, ocena=0, prosecna_ocena=0, prosecna_ocena_korisnika=0)
        poseta.save()
        
        for p in posetioci:
            pozivnica = Pozivnica(korisnik = p)
            pozivnica.save()
            
            #poslati mail svakom od njih!
            link = reverse('profil')
            adresa = self.request.META['HTTP_HOST']+link
        
            send_mail('Reservation in a restaurant', 'Accept or decline ' + korisnik.user.username + "'s reservation in "+ restoran.naziv +' with this link http://'+adresa, settings.EMAIL_HOST_USER,[p.user.email])
              
            poseta.zvanice.add(pozivnica)

        return response
    
class PosetaDetail(DetailView):
    model = Poseta
    template_name = 'restoran/poseta.html'
    context_object_name = 'poseta'
    
    def get_context_data(self, **kwargs):
        context = super(PosetaDetail, self).get_context_data(**kwargs)
        korisnik = Korisnik.objects.get(user__pk = self.request.user.pk)
        
        context["user"] = korisnik
        
        return context

class UpdateKorisnik(UpdateView):
    model = Korisnik
    template_name = 'restoran/imageupload.html'
    form_class = ImageUploadForm
    
    def get_success_url(self):
        return reverse('profil')
    
def friend_profile(request, pk):
    user = request.user
    korisnik = Korisnik.objects.get(user__pk = user.pk)
    
    prijatelj = get_object_or_404(Korisnik, pk=pk)
    
    context = {'korisnik': korisnik, 'prijatelj':prijatelj}
    
    if prijatelj in korisnik.prijatelji.all():
        context["addfriend"] = False
    else:
        context["addfriend"] = True
    
    try:
        value = request.GET['sort_by']
        context['prijatelji'] = sort_friend_list(value, prijatelj)
    except MultiValueDictKeyError:
        context['prijatelji'] = prijatelj.prijatelji.all()
    
    
    return render(request, 'restoran/prijateljprofil.html', context)

def reorder(request, pk):
    user = request.user
    korisnik = Korisnik.objects.get(user__pk = user.pk)
    
    restoran = get_object_or_404(Restoran, pk=pk)
        
    context = {'user':korisnik, 'restoran':restoran}
    return render(request, 'restoran/reorder.html', context)
    
def fill_data(request):
    response_data={}
    
    pk = request.GET['pk']
    
    restoran = get_object_or_404(Restoran, pk=pk)
    
    for sto in restoran.stolovi.all():
        response_data[sto.pk] = {"stolice":sto.broj_stolica, "stanje":sto.stanje, "red":sto.red, "kolona":sto.kolona}
        
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def update(request):
    response_data={}
    
    restoran_pk = request.GET['pk']
    number = request.GET['number']
    sto_pk = request.GET['stolice']
    kolona = request.GET['kolona']
    vrsta = request.GET['vrsta']
    
    if int(number) > 0:
        restoran = get_object_or_404(Restoran, pk=restoran_pk)
        if sto_pk != "":
            for sto in restoran.stolovi.all():
                if sto.pk == int(sto_pk):
                    sto.broj_stolica = number
                    sto.save()
                    response_data[sto.pk] = {"stolice":sto.broj_stolica, "stanje":sto.stanje, "red":sto.red, "kolona":sto.kolona}
                    break
        else:
            sto = Sto(broj_stolica=int(number),  red=int(vrsta), kolona=int(kolona))
            sto.save()
            restoran.stolovi.add(sto)
        
            response_data[sto.pk] = {"stolice":sto.broj_stolica, "stanje":sto.stanje, "red":sto.red, "kolona":sto.kolona}
    
    return HttpResponse(json.dumps(response_data), content_type="application/json")
    
def delete(request):
    response_data={}
    
    restoran_pk = request.GET['pk']
    sto_pk = request.GET['stolice']
    
    restoran = get_object_or_404(Restoran, pk=restoran_pk)
    for sto in restoran.stolovi.all():
        if sto.pk == int(sto_pk):
            response_data[sto.pk] = {"red":sto.red, "kolona":sto.kolona}
            sto.delete()
    
    return HttpResponse(json.dumps(response_data), content_type="application/json")


def check(request):
    response_data={}
    
    restoran_pk = request.GET['pk']
    #2015-12-29 12:15:41
    string_date = request.GET['value']
    
    zauzece = request.GET['zauzece']
    zauzece = int(zauzece)
    datum = datetime.datetime.strptime(string_date, "%Y-%m-%d %H:%M:%S")
    datum = timezone.make_aware(datum,timezone.get_default_timezone())
    datum = datum.astimezone(timezone.utc)

    restoran = get_object_or_404(Restoran, pk=restoran_pk)
    rezervacije = Rezervacija.objects.filter(restoran__pk=restoran.pk)

    #naci sta je slobodno nakon posaltog datuma
    for rezervacija in rezervacije:
        for sto in rezervacija.stolovi.all():
            if not (datum < rezervacija.datum or datum > rezervacija.datum + datetime.timedelta(hours=rezervacija.zauzece)):
            
                show = "Date of reservation: {} \nTaken until: {}h".format(rezervacija.datum.strftime("%d-%m-%Y %H:%M"), 
                                                                         (rezervacija.datum + datetime.timedelta(hours=rezervacija.zauzece))
                                                                         .strftime("%d-%m-%Y %H:%M"))
                
                
                response_data[sto.pk] = {"stolice":sto.broj_stolica, "stanje":'R', "red":sto.red, "kolona":sto.kolona, 'zauzet':show}
            else:
                response_data[sto.pk] = {"stolice":sto.broj_stolica, "stanje":'F', "red":sto.red, "kolona":sto.kolona, 'zauzet':''}
                
    for sto in restoran.stolovi.all():
        if not response_data.has_key(sto.pk): 
            response_data[sto.pk] = {"stolice":sto.broj_stolica, "stanje":'F', 
                                     "red":sto.red, "kolona":sto.kolona, 'zauzet':''}
        
    
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def rezervisani_stolovi(request):
    response_data={}
    
    poseta_pk = request.GET['pk']
    
    poseta = get_object_or_404(Poseta, pk=poseta_pk)

    #naci sta je slobodno nakon posaltog datuma
    
    for sto in [sto for sto in poseta.rezervacija.stolovi.all()]:
        response_data[sto.pk] = {"stolice":sto.broj_stolica, "stanje":sto.stanje, "red":sto.red, "kolona":sto.kolona} 

    return HttpResponse(json.dumps(response_data), content_type="application/json")       
            
def stanje_svih_stolova(request):
    response_data={}
    
    restoran_pk = request.GET['pk']

    restoran = get_object_or_404(Restoran, pk=restoran_pk)
    rezervacije = Rezervacija.objects.filter(restoran__pk=restoran.pk)

    #naci sta je slobodno nakon posaltog datuma
    for rezervacija in rezervacije:
        if datetime.datetime.now() < rezervacija.datum.replace(tzinfo=None) + datetime.timedelta(hours=rezervacija.zauzece):
            for sto in rezervacija.stolovi.all():
                
                show = "Date of reservation: {} \nTaken until: {}h".format(rezervacija.datum.strftime("%d-%m-%Y %H:%M"), 
                                                                         (rezervacija.datum + datetime.timedelta(hours=rezervacija.zauzece)).strftime("%d-%m-%Y %H:%M"))
                
                response_data[sto.pk] = {"stolice":sto.broj_stolica, "stanje":'R', 
                                         "red":sto.red, "kolona":sto.kolona, 'zauzet':show}
                
    for sto in restoran.stolovi.all():
        if not response_data.has_key(sto.pk): 
            response_data[sto.pk] = {"stolice":sto.broj_stolica, "stanje":'F', 
                                     "red":sto.red, "kolona":sto.kolona, 'zauzet':''}
    
    return HttpResponse(json.dumps(response_data), content_type="application/json")
    