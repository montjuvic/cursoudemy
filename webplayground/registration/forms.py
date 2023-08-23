from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class UserCreationFormWithEmail(UserCreationForm):
    email = forms.EmailField(
        required=True, help_text="Requerido, 254 chars como maximo y debe ser valido")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):  # para validar el email, que no hayan 2 usuarios con el mismo
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("El email ya esta registrado")
        return email

class ProfileForm(forms.ModelForm):

    class Meta:
        model=Profile
        fields = ['avatar','bio','link']

        widgets= {
            "avatar":forms.ClearableFileInput(
        attrs={'class': 'form-control-file mt-3'}),

            "bio": forms.Textarea(
        attrs={'class': 'form-control', 'rows': 3, 'placeholder':'Escribe tu biografia'}),

            "link": forms.URLInput(
        attrs={'class': 'form-control', 'placeholder':'Escoge el enlace'}),

        }  
        labels = {
            'avatar':'','bio':'','link':'',
        }

class EmailForm(forms.ModelForm):
    email = forms.EmailField(
    required=True, help_text="Requerido, 254 chars como maximo y debe ser valido")

    
    class Meta:
        model=User
        fields = ['email']
        
    def clean_email(self):  # para validar el email, que no hayan 2 usuarios con el mismo
        email = self.cleaned_data.get("email")

        if 'email' in self.changed_data: #lista que almacena los DATOS que se han editado en el formulario
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError("El email ya esta registrado")
        return email