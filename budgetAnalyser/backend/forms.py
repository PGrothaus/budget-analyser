import json

from django import forms

from .models import Transaction
from .models import Bank
from .models import Account


class UploadTransactionsForm(forms.Form):

    file = forms.FileField()
    bank = forms.ModelChoiceField(queryset=Bank.objects.none())
    account = forms.ModelChoiceField(queryset=Account.objects.none())

    def __init__(self, user, *args, **kwargs):
        super(UploadTransactionsForm, self).__init__(*args, **kwargs)
        self.fields['bank'].queryset = Bank.objects.filter(user=user)
        self.fields['account'].queryset = Account.objects.filter(user=user)
