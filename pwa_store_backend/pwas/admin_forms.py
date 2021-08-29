import json
from django import forms
from .models import Pwa

class PwaAdminForm(forms.ModelForm):
    class Meta:
        model = Pwa
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        if instance and instance.manifest_json:
            instance.manifest_json = json.loads(instance.manifest_json)
        super().__init__(*args, **kwargs)

    def clean_manifest_json(self):
        manifest_json = self.cleaned_data['manifest_json']
        return json.dumps(manifest_json)
