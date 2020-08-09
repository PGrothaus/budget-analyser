import json

from django import forms

from backend.models import Category
from prettyjson import PrettyJSONWidget


class CreateCategorizationRuleForm(forms.Form):

    name = forms.CharField(max_length=50)
    rule = forms.CharField(max_length=1024, widget=PrettyJSONWidget())
    effect_value = forms.ModelChoiceField(queryset=Category.objects.all(), initial=0)

    def clean_rule(self):
        jdata = self.cleaned_data["rule"]
        try:
            json_data = json.loads(jdata)
        except Exception as e:
            print("ERROR in json format")
            print("Incoming string", jdata)
            print(e)
            raise forms.ValidationError("Invalid data in jsonfield")
        return jdata
