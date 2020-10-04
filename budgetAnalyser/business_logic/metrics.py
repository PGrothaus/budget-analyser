from django.db.models import Sum
from datetime import datetime
from datetime import timedelta

from backend.models import AssetValue
from backend.models import Account
from backend.models import AccountValue
from backend.models import Bank
from backend.models import Currency
from backend.models import ExchangeRate
from backend.models import NetWorth
from backend.models import Transaction

from . import helpers


def recalculate(user, kind, starting):
    fcts = {
        "networth": networth,
        "savings": savings,
        "retirement": retirement,
        "retirement_investment": retirement_investments,
    }
    nws = NetWorth.objects.filter(type=kind, valued_at__gte=starting,)
    print("Recalculate %s starting at %s" % (kind, starting))
    for nw in nws:
        nw.value = fcts[kind](user, when=nw.valued_at)
        nw.save()


def networth(user, when=None, to_currency="CLP"):
    acc_vals = get_all_account_values(user, when=when)
    asset_vals = get_asset_values(user, when=when)
    credit_vals = get_credit_vals(user, when=when)
    nw = sum_value_in_currency(acc_vals, when, to_currency)
    nw += sum_value_in_currency(asset_vals, when, to_currency)
    nw -= sum_value_in_currency(credit_vals, when, to_currency)
    return nw


def retirement(user, when=None, to_currency="CLP"):
    acc_vals = get_retirement_account_values(user, when)
    return sum_value_in_currency(acc_vals, when, to_currency)


def savings(user, when=None, to_currency="CLP"):
    acc_vals = get_savings_account_values(user, when)
    return sum_value_in_currency(acc_vals, when, to_currency)


def retirement_investments(user, when=None):
    print("Calculate retirement investments from %s" % when)
    accs = get_all_retirement_accounts(user)
    total = 0
    for acc in accs:
        val = invested_money(acc, when=when)
        print("Invested %s in account %s" % (val, acc.name))
        if val is None:
            continue
        total += val
    return total


def update_retirement_investments(user, starting):
    print("Update retirement starting at %s" % starting)
    elems = NetWorth.objects.filter(
        user=user, type="retirement_investment", valued_at__gte=starting,
    )
    for elem in elems:
        elem.value = retirement_investments(user, when=elem.valued_at)
        print("Retirement investment at %s is %s" % (elem.valued_at, elem.value))
        elem.save()


def update_savings_investments(user, starting):
    print("Update savings investments starting at %s" % starting)
    elems = NetWorth.objects.filter(
        user=user, type="savings_investment", valued_at__gte=starting,
    )
    for elem in elems:
        elem.value = savings_investments(user, when=elem.valued_at, include_normal=True)
        elem.save()


def savings_investments(user, when=None, include_normal=False):
    print("Calculate savings investments from %s" % when)
    accs = get_all_savings_accounts(user)
    total = 0
    for acc in accs:
        val = invested_money(acc, include_normal=include_normal, when=when)
        if val is None:
            continue
        # print("Individual investment value", acc.id, acc.name, val)
        total += val
    return total


def get_all_savings_accounts(user):
    return Account.objects.filter(user=user, type__type__in=["NORMAL", "INVESTMENT"])


def get_all_retirement_accounts(user):
    accs = Account.objects.filter(user=user, type__type__in=["RETIREMENT"])
    print("Retirement accounts:", [acc.name for acc in accs])
    return accs


def get_savings_account_values(user, when=None):
    return get_account_values(user, ["NORMAL", "INVESTMENT"], when)


def get_retirement_account_values(user, when=None):
    return get_account_values(user, ["RETIREMENT"], when)


def get_credit_vals(user, when=None):
    return get_account_values(user, ["CREDIT"], when)


def get_all_account_values(user, when=None):
    if not when:
        when = datetime.utcnow()
    return (
        AccountValue.objects.filter(user=user, valued_at__lte=when,)
        .exclude(account__type__type="CREDIT")
        .order_by("account__name", "account__bank__id", "-valued_at")
        .distinct("account__name", "account__bank__id")
    )


def get_account_values(user, kind, when=None):
    if not when:
        when = datetime.utcnow()
    return (
        AccountValue.objects.filter(
            user=user, account__type__type__in=kind, valued_at__lte=when,
        )
        .order_by("account__name", "account__bank__id", "-valued_at")
        .distinct("account__name", "account__bank__id")
    )


def get_asset_values(user, when=None):
    if not when:
        when = datetime.utcnow()
    return (
        AssetValue.objects.filter(user=user, valued_at__lte=when,)
        .order_by("asset__name", "-valued_at")
        .distinct("asset__name",)
    )


def sum_value_in_currency(accVals, when, to_currency="CLP"):
    total = 0
    for accVal in accVals:
        account_value_to_target_currency(accVal, when, to_currency)
        total += accVal.value
    return total


def account_value_to_target_currency(
    acc_val, when=None, to_currency="CLP",
):
    target_cur = Currency.objects.get(code=to_currency)
    if hasattr(acc_val, "account"):
        cur_currency_code = acc_val.account.currency.code
    elif hasattr(acc_val, "asset"):
        cur_currency_code = acc_val.asset.currency.code
    else:
        raise AttributeError("Missing a required attr here.")
    if cur_currency_code != to_currency:
        # when = acc_val.valued_at if when is None else when
        rates = get_all_exchange_rates(to_currency, when)
        rate = [elem.rate for elem in rates if elem.origin.code == cur_currency_code][0]
        if hasattr(acc_val, "account"):
            acc_val.account.currency = target_cur
        elif hasattr(acc_val, "asset"):
            acc_val.asset.currency = target_cur
        else:
            raise AttributeError("Missing a required attr here...")
        acc_val.value = rate * acc_val.value


def get_all_exchange_rates(target_code, when):
    if not when:
        when = datetime.utcnow()
    return (
        ExchangeRate.objects.filter(target__code=target_code, valued_at__lte=when,)
        .order_by("origin__code", "target__code", "-valued_at")
        .distinct("origin__code", "target__code")
    )


def invested_money(account, include_normal=False, when=None):
    if account.type.id == 2 and not include_normal:
        return None
    if not when:
        when = datetime.utcnow()
    if account.type.id == 2:
        elems = AccountValue.objects.filter(
            account_id=account.id, valued_at__lte=when,
        ).order_by("-valued_at")
        if not elems:
            return 0
        val = elems[0].value
        return helpers.exchange(val, account.currency.code, "CLP", when)
    val_in = (
        Transaction.objects.filter(account_id=account.id, date__lte=when,)
        .exclude(type="expense")
        .aggregate(total=Sum("amount"))["total"]
    )

    val_out = Transaction.objects.filter(
        account_id=account.id, date__lte=when, type="expense"
    ).aggregate(total=Sum("amount"))["total"]

    if val_in is None:
        return None
    tmp = Transaction.objects.filter(account_id=account.id)[0]
    val_out = 0 if val_out is None else val_out
    delta = val_in - val_out
    return helpers.exchange(delta, tmp.currency, "CLP", when)
