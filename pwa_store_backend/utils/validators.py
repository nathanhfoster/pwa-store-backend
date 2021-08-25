from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import json

def validate_json(string):
    try:
        json_object = json.loads(string)
        return False
    except ValueError as e:
        return True


class HasValidJson:
    def __init__(self, base):
        self.base = base

    def __call__(self, value):
        if validate_json(value):
            raise ValidationError("manifest_json is not a valid JSON")