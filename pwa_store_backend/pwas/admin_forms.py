import json
from django import forms
from .models import Pwa

class PwaAdminForm(forms.ModelForm):
    class Meta:
        model = Pwa
        fields = '__all__'
