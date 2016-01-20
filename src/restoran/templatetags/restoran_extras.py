'''
Created on 16 Nov 2015

@author: Chakmi
'''
from django import template
from restoran.models import Ocena


register = template.Library()

@register.filter
def isfriend(queryset):             # return ValuesQuerySet object
    items = queryset.values('id')
    retlist = []

    for item in items:
        for k, v in item.items(): #raspakivanje vrednosti, posto .items funkcija vraca key-value par
            retlist.append(v)
    
    return retlist

@register.filter
def lepdatum(now):
    return now.strftime("%d-%m-%Y %H:%M")

@register.filter
def prosecna_ocena_prijatelja(user):
    ocene = Ocena.objects.all()
    
    for ocena in ocene:
        if ocena.ocenjivac.pk == user:
            return True
    
    return False
