from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
import datetime

STATE = (
         ('A', 'Accepted'),
         ('D', 'Decline'),
         ('P', 'Pending')
    )

TABLE_STATE = (
         ('R', 'Reserved'),
         ('F', 'Free')
    )

# Create your models here.
class Korisnik(models.Model):
    user = models.OneToOneField(User,related_name='user_auth')
    prijatelji =  models.ManyToManyField("self", blank=True)
    picture = models.ImageField(upload_to = 'pic_folder', default = 'pic_folder/no-img.jpg',blank = True, null = True)
    
    def __unicode__(self):
        return self.user.username
    
class VrstaRestorana(models.Model):
    naziv = models.CharField(blank=False, null=False, max_length=20)
    opis = models.CharField(blank=False, null=False, max_length=200)
    
    def __unicode__(self):
        return self.naziv
    
class Jelo(models.Model):
    naziv = models.CharField(blank=False, null=False, max_length=20)
    opis = models.CharField(blank=False, null=False, max_length=200)
    cena = models.FloatField(blank=False, null=False)
    
    def __unicode__(self):
        return self.naziv

class Ocena(models.Model):
    ocena = models.IntegerField()
    ocenjivac = models.ForeignKey(Korisnik, blank=False, null=False)
    
    def __unicode__(self):
        return self.ocenjivac.user.username

class Sto(models.Model):
    stanje = models.CharField(max_length=1, choices=TABLE_STATE, default='F')
    broj_stolica = models.IntegerField(default=0, blank=False, null=False)
    red = models.IntegerField(default=0, blank=False, null=False)
    kolona = models.IntegerField(default=0, blank=False, null=False)
    
    def __unicode__(self):
        return "("+str(self.red)+","+str(self.kolona)+")_____"+str(self.broj_stolica)
    
class Restoran(models.Model):
    naziv = models.CharField(blank=False,null=False, max_length=20)
    adresa = models.CharField(blank=False, max_length=70, default="")
    tip = models.ForeignKey(VrstaRestorana, blank=False, null=False)
    jelovnik = models.ManyToManyField(Jelo, blank=False)
    lat = models.FloatField(blank=False, default=0)
    lon = models.FloatField(blank=False, default=0)
    menadzer = models.ManyToManyField(Korisnik, blank=False)
    ocene = models.ManyToManyField(Ocena, blank=True)
    stolovi = models.ManyToManyField(Sto, blank=True)
    
    def __unicode__(self):
        return unicode(self.naziv)

class Pozivnica(models.Model):
    korisnik = models.ForeignKey(Korisnik, blank=False, null=False, related_name='pozvani')
    stanje = models.CharField(max_length=1, choices=STATE, default='P')
    ocena = models.IntegerField(default=0)
    
    def getstanje(self):
        for t in STATE:
            if(t[0] == self.stanje):
                return t[1]
    
    def __unicode__(self):
        return self.korisnik.user.username+"|"+self.stanje

class Rezervacija(models.Model):
    korisnik = models.ForeignKey(Korisnik, blank=False, null=False, related_name='korisnik')
    restoran = models.ForeignKey(Restoran, blank=False, null=False)
    datum = models.DateTimeField('date published', unique = True)
    zauzece = models.IntegerField(blank=False, null=False)
    zvanice = models.ManyToManyField(Korisnik, related_name='zvanice', blank=True)
    stolovi = models.ManyToManyField(Sto, related_name='stolovi', blank=True)
    
    def __unicode__(self):
        return self.korisnik.user.username+"|"+self.restoran.naziv
    
class Poseta(models.Model):
    rezervacija = models.ForeignKey(Rezervacija, blank=False, null=False)
    ocena = models.IntegerField()
    prosecna_ocena = models.FloatField()
    prosecna_ocena_korisnika = models.FloatField()
    zvanice = models.ManyToManyField(Pozivnica, related_name='zvanice')
    
    def __unicode__(self):
        return self.rezervacija.korisnik.user.username
    
    def was_done_recently(self):
        zauzece = self.rezervacija.zauzece
        return timezone.now()  > self.rezervacija.datum + datetime.timedelta(hours=zauzece)    