from backend.models import AssetValue
from backend.models import Account
from backend.models import AccountValue
from backend.models import Bank
from backend.models import Currency
from backend.models import ExchangeRate
from backend.models import Transaction


def networth(user):

    acc_vals = get_account_values(user)
    asset_vals = get_asset_values(user)
    credit_vals = get_credit_vals(user)
    nw = account_values_to_target_currency(acc_vals)
    nw += asset_values_to_target_currency(asset_vals)
    nw -= account_values_to_target_currency(credit_vals)
    return nw

def get_account_values(user):
    return AccountValue.objects.filter(
        user=user
        ).exclude(
            account__type__type='CREDIT'
        ).order_by(
            'account__name', 'account__bank__id', '-valued_at'
        ).distinct(
            'account__name', 'account__bank__id'
        )

def get_credit_vals(user):
    return AccountValue.objects.filter(
        user=user
        ).filter(
            account__type__type='CREDIT'
        ).order_by(
            'account__name', 'account__bank__id', '-valued_at'
        ).distinct(
            'account__name', 'account__bank__id'
        )

def get_asset_values(user):
    return AssetValue.objects.filter(
        user=user
        ).order_by(
            'asset__name', '-valued_at'
        ).distinct(
            'asset__name',
        )

def account_values_to_target_currency(acc_vals,
                                      target_currency_code="CLP"):
    rates = ExchangeRate.objects.filter(
        target__code=target_currency_code
    ).order_by(
        'origin__code', 'target__code', '-valued_at'
    ).distinct(
        'origin__code', 'target__code'
    )
    target_cur = Currency.objects.get(code=target_currency_code)
    nw = 0
    for acc_val in acc_vals:
        cur_currency_code = acc_val.account.currency.code
        if not cur_currency_code == target_currency_code:
            rate = [elem.rate for elem in rates if elem.origin.code == cur_currency_code][0]
            acc_val.account.currency = target_cur
            acc_val.value = rate * acc_val.value
        nw += acc_val.value
    return nw

def asset_values_to_target_currency(acc_vals,
                                    target_currency_code="CLP"):
    rates = ExchangeRate.objects.filter(
        target__code=target_currency_code
    ).order_by(
        'origin__code', 'target__code', '-valued_at'
    ).distinct(
        'origin__code', 'target__code'
    )
    target_cur = Currency.objects.get(code=target_currency_code)
    nw = 0
    for acc_val in acc_vals:
        cur_currency_code = acc_val.asset.currency.code
        if not cur_currency_code == target_currency_code:
            rate = [elem.rate for elem in rates if elem.origin.code == cur_currency_code][0]
            acc_val.asset.currency = target_cur
            acc_val.value = rate * acc_val.value
        nw += acc_val.value
    return nw
