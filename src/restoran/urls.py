'''
Created on 8 Nov 2015

@author: Chakmi
'''
from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^restorani/$', views.RestoraniList.as_view(), name='restorani'),
    url(r'^restoran/(?P<pk>\d+)/$', views.RestoranDetail.as_view(), name='restoran'),
    url(r'^jelo/(?P<pk>\d+)/$', views.JeloDetail.as_view(), name='jelo'),
    #url(r'^prijatelji/(?P<pk>\d+)/$', views.prijatelji, name='prijatelji'),
    url(r'^prijatelji/$', views.prijatelji, name='prijatelji'),
    
    url(r'^searchfriends/$', views.searchfriends, name='searchfriends'),
    url(r'^dodajprijatelja/$', views.dodajprijatelja, name='dodajprijatelja'),
    
    url(r'^tiprestorana/(?P<pk>\d+)/$', views.TipRestoranaDetail.as_view(), name='tiprestorana'),
    url(r'^rezervacija/(?P<pk>\d+)/$', views.CreateRezervacija.as_view(), name='rezervacija'),
    url(r'^poseta/(?P<pk>\d+)/$', views.PosetaDetail.as_view(), name='poseta'),
    
    url(r'^unfriend/(?P<pk>\d+)/$', views.unfriend, name='unfriend'),
    url(r'^oceni/(?P<pk>\d+)/$', views.oceni, name='oceni'),
    
    url(r'^prihvati/(?P<pk>\d+)/$', views.prihvati, name='prihvati'),
    url(r'^odustani/(?P<pk>\d+)/$', views.odustani, name='odustani'),
    
    url(r'^ocenipoziv/(?P<pk>\d+)/$', views.ocenipoziv, name='ocenipoziv'),
    
    url(r'^izmenarestorana/(?P<pk>\d+)/$', views.izmenarestorana, name='izmenarestorana'),
    url(r'^updatejelo/(?P<pk>\d+)/$', views.JeloUpdate.as_view(), name='updatejelo'),
    url(r'^deletejelo/(?P<pk>\d+)/$', views.JeloDelete.as_view(), name='deletejelo'),
    url(r'^createjelo/(?P<pk>\d+)/$', views.JeloCreate.as_view(), name='createjelo'),
    
    url(r'^imageupload/(?P<pk>\d+)/$', views.UpdateKorisnik.as_view(), name='imageupload'),
    
    url(r'^friendprofile/(?P<pk>\d+)/$', views.friend_profile, name='friendprofile'),
    url(r'^reorder/(?P<pk>\d+)/$', views.reorder, name='reorder'),
    url(r'^fill_data/$', views.fill_data, name='fill_data'),
    url(r'^update/$', views.update, name='update'),
    url(r'^delete/$', views.delete, name='delete'),
    url(r'^check/$', views.check, name='check'),
    url(r'^stanje_svih_stolova/$', views.stanje_svih_stolova, name='stanje_svih_stolova'),
    url(r'^rezervisani_stolovi/$', views.rezervisani_stolovi, name='rezervisani_stolovi'),
]