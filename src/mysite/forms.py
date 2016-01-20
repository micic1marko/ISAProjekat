'''
Created on 10 Nov 2015

@author: Chakmi
'''
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from restoran.models import Korisnik
from restoran.views import prijatelji


class RegistrationForm(UserCreationForm):
    username = forms.CharField(required = True)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required = False)
    last_name = forms.CharField(required = False)
    
    class Meta:
        model = User
        fields = ['first_name','last_name', 'username', 'email', 'password1', 'password2',]
        
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget.attrs['class']='form-control'
        self.fields["first_name"].widget.attrs['class']='form-control'
        self.fields["last_name"].widget.attrs['class']='form-control'
        self.fields["email"].widget.attrs['class']='form-control'  
        self.fields["password1"].widget.attrs['class']='form-control' 
        self.fields["password2"].widget.attrs['class']='form-control' 
        
    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit = False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()

        return user
    
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email']
        
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
