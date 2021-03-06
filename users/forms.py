from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Contact

class UserRegisterationForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        
class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        widgets = {
          'message': forms.Textarea(attrs={'rows':5, 'cols':15}),
        }
        fields = '__all__'