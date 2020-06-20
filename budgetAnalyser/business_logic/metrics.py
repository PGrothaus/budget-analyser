from django.db.models import Sum

from backend.models import AssetValue
from backend.models import Account
from backend.models import AccountValue
from backend.models import Bank
from backend.models import Currency
from backend.models import ExchangeRate
from backend.models import Transaction

from . import helpers


def networth(user):

    acc_vals = get_account_values(user)
    asset_vals = get_asset_values(user)
    credit_vals = get_credit_vals(user)
    nw = account_values_to_target_currency(acc_vals)
    nw += asset_values_to_target_currency(asset_vals)
    nw -= account_values_to_target_currency(credit_vals)
    return nw


def retirement(user):
    acc_vals = get_retirement_account_values(user)
    return account_values_to_target_currency(acc_vals)


def retirement_investments(user):
    accs = get_all_retirement_accounts(user)
    total = 0
    for acc in accs:
        val = invested_money(acc)
        if val is None:
            continue
        total += val
    return total


def savings(user):
    acc_vals = get_savings_account_values(user)
    return account_values_to_target_currency(acc_vals)


def savings_investments(user):
    accs = get_all_savings_accounts(user)
    total = 0
    for acc in accs:
        val = invested_money(acc, include_normal=True)
        if val is None:
            continue
        print(acc.id, acc.name, val)
        total += val
    return total


def get_all_savings_accounts(user):
    return Account.objects.filter(user=user, type__type__in=["NORMAL", "INVESTMENT"])


def get_all_retirement_accounts(user):
    return Account.objects.filter(user=user, type__type__in=["RETIREMENT"])


def get_savings_account_values(user):
    return AccountValue.objects.filter(
            user=user,
            account__type__type__in=["NORMAL", "INVESTMENT"]
        ).order_by(
            'account__name', 'account__bank__id', '-valued_at'
        ).distinct(
            'account__name', 'account__bank__id'
        )


def get_retirement_account_values(user):
    return AccountValue.objects.filter(
            user=user,
            account__type__type="RETIREMENT"
        ).order_by(
            'account__name', 'account__bank__id', '-valued_at'
        ).distinct(
            'account__name', 'account__bank__id'
        )


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


def invested_money(account, include_normal=False):
    if account.type.id == 2 and not include_normal:
        return None
    if account.type.id == 2:
        elems = AccountValue.objects.filter(
            account_id=account.id
            ).order_by(
                '-valued_at'
            )
        if not elems:
            return 0
        val = elems[0].value
        return helpers.exchange(val, account.currency.code, "CLP")
    val_in = Transaction.objects.filter(
        account_id=account.id,
    ).exclude(
        type='expense'
    ).aggregate(
        total=Sum('amount')
    )["total"]

    val_out = Transaction.objects.filter(
        account_id=account.id,
        type='expense'
    ).aggregate(
        total=Sum('amount')
    )["total"]

    if val_in is None:
        return None
    tmp = Transaction.objects.filter(
        account_id=account.id)[0]
    val_out = 0 if val_out is None else val_out
    delta = val_in - val_out
    return helpers.exchange(delta, tmp.currency, "CLP")
