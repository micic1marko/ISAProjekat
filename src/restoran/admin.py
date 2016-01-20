from django.contrib import admin

from . import models


# Register your models here.
admin.site.register(models.Korisnik)
admin.site.register(models.VrstaRestorana)
admin.site.register(models.Jelo)
admin.site.register(models.Restoran)
admin.site.register(models.Rezervacija)
admin.site.register(models.Poseta)
admin.site.register(models.Pozivnica)
admin.site.register(models.Ocena)
admin.site.register(models.Sto)