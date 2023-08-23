from django import forms
from .models import Page

class PageForm(forms.ModelForm):

    class Meta:
        model = Page
        fields = ["title", "content", "order"]

        widgets= {
            "title":forms.TextInput(
        attrs={'class': 'form-control', 'placeholder':'Escribe tu titulo'}),

            "content": forms.Textarea(
        attrs={'class': 'form-control', 'rows': 3}),

            "order": forms.NumberInput(
        attrs={'class': 'form-control', 'placeholder':'Escoge el ordenm'}),

        }
        labels = {
            'title':'','content':'','order':'',
        }