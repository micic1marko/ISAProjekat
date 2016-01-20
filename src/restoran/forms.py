'''
Created on 8 Nov 2015

@author: Chakmi
'''
from datetimewidget.widgets import DateTimeWidget
from django import forms
from django.forms import widgets
from gmapi.forms.widgets import GoogleMap

from restoran.models import Korisnik, Rezervacija, Jelo, Sto




class LoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    lozinka = forms.CharField(label='Lozinka')
    
    class Meta:
        model = Korisnik
        fields = ['first_name','last_name', 'username', 'email', 'password1', 'password2',]
        
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget.attrs['class']='form-control'        
        self.fields["first_name"].widget.attrs['class']='form-control'
        self.fields["last_name"].widget.attrs['class']='form-control'
        self.fields["email"].widget.attrs['class']='form-control'  
        self.fields["password1"].widget.attrs['class']='form-control' 
        self.fields["password2"].widget.attrs['class']='form-control' 
    
class SearchFriendsForm(forms.Form):
    text = forms.CharField(label='text')
    #user_pk = forms.IntegerField(label='user_pk')
    
class AddFriendsForm(forms.Form):
    user_pk = forms.IntegerField(label='user_pk')
    friend_pk = forms.IntegerField(label='friend_pk')
    
class OceniForm(forms.Form):
    ocena = forms.IntegerField(label='ocena')
    
class MapForm(forms.Form):
    map = forms.Field(widget=GoogleMap(attrs={'width':710, 'height':310}))
    
class RezervacijaForm(forms.ModelForm):
    datum = forms.DateTimeField(widget=DateTimeWidget(usel10n=True, bootstrap_version=3), label='Date')
    zauzece = forms.IntegerField(required = True , label='Taken for')
    zvanice = forms.ModelMultipleChoiceField(Korisnik, label='Invites', required = False)
    stolovi = forms.ModelMultipleChoiceField(Sto, label='', required = True)
    
    class Meta:
        model = Rezervacija
        fields = ['datum','zauzece','zvanice', 'stolovi']  
        
    def __init__(self, *args, **kwargs):
        super(RezervacijaForm, self).__init__(*args, **kwargs)
        self.fields["datum"].widget.attrs['class']='form-control'
        self.fields["datum"].widget.attrs['id']='datum'
        #self.fields["datum"].widget = DateTimeWidget(usel10n = True, bootstrap_version=3)       
        self.fields["zauzece"].widget.attrs['class']='form-control'
        self.fields["zvanice"].widget.attrs['class']='form-control'
        #self.fields["stolovi"].widget.attrs['hidden']='true'
        
class JeloUpdateForm(forms.ModelForm):
    class Meta:
        model = Jelo
        fields=['naziv', 'opis', 'cena']
        
    def __init__(self, *args, **kwargs):
        super(JeloUpdateForm, self).__init__(*args, **kwargs)
        self.fields["opis"].widget.attrs['class']='form-control'
        #self.fields["datum"].widget = DateTimeWidget(usel10n = True, bootstrap_version=3)       
        self.fields["naziv"].widget.attrs['class']='form-control'
        self.fields["cena"].widget.attrs['class']='form-control'
        
class ImageUploadForm(forms.ModelForm):
    """Image upload form."""
    picture = forms.ImageField()
    
    class Meta:
        model = Korisnik
        fields = ['picture']
        
    def __init__(self, *args, **kwargs):
        super(ImageUploadForm, self).__init__(*args, **kwargs)
        self.fields["picture"].widget.attrs['class']='form-control'