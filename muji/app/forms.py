from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=200)
    first_name = forms.CharField(max_length=64)
    last_name = forms.CharField(max_length=64)
    address = forms.CharField(max_length=256)
    phone_number  = forms.CharField(max_length=15)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'address', 'phone_number','password1', 'password2', )

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['email', 'first_name', 'last_name', 'address', 'phone_number']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }

class WishlistForm(forms.Form):
    item_id = forms.IntegerField(widget=forms.HiddenInput())