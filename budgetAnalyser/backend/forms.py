import json

from django import forms

from .models import Account
from .models import Bank
from .models import Currency
from .models import ExchangeRate
from .models import Transaction




class UploadTransactionsForm(forms.Form):

    file = forms.FileField()
    bank = forms.ModelChoiceField(queryset=Bank.objects.none())
    account = forms.ModelChoiceField(queryset=Account.objects.none())

    def __init__(self, user, *args, **kwargs):
        super(UploadTransactionsForm, self).__init__(*args, **kwargs)
        self.fields['bank'].queryset = Bank.objects.filter(user=user).order_by('name')
        self.fields['account'].queryset = Account.objects.filter(user=user, type=2).order_by('bank__name', 'name')


class InvestmentForm(forms.Form):

    account = forms.ModelChoiceField(queryset=Account.objects.none())
    date = forms.DateTimeField()
    price_in_CLP = forms.FloatField()
    amount_in_account_CURRENCY = forms.FloatField()
    is_income = forms.BooleanField(required=False)

    def __init__(self, user, *args, **kwargs):
        super(InvestmentForm, self).__init__(*args, **kwargs)
        self.fields['account'].queryset = Account.objects.filter(user=user, type__in=[1, 3]).order_by('bank__name', 'name')
