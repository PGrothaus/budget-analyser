import pytz
from datetime import datetime

from django.db import IntegrityError

from . import helpers
from . import parsers
from . import queries
from . import utils
from . import extractors
from . import metrics
from backend.models import AccountValue
from backend.models import Currency
from backend.models import ExchangeRate
from backend.models import Transaction
from backend.models import UploadedFile


def handle_transactions_upload(request):
    bank = queries.bank_from_request(request)
    account = queries.account_from_request(request)
    uploaded_at = pytz.utc.localize(datetime.now())
    filepath = helpers.filepath_to_store_uploaded_transaction(
        request.user, bank, account, uploaded_at)
    entry_file = _add_entry_to_uploaded_files_table(
        request.user, account, uploaded_at)
    utils.save_uploaded_file(filepath, request.FILES['file'])
    _save_account_values_from_file_to_db(
        filepath, account, request.user, entry_file)
    transactions_new, transactions_old = _save_transactions_from_file_to_db(
        filepath, account, request.user, entry_file)

    _apply_rules_to_uncategorized_transactions(request)
    all_trans = transactions_new + transactions_old
    print(all_trans)
    firstTransaction = sorted(all_trans, key=lambda elem: elem["date"])[0]
    when = firstTransaction["date"]
    metrics.recalculate(request.user, "networth", when)
    metrics.recalculate(request.user, "savings", when)
    metrics.recalculate(request.user, "retirement", when)
    metrics.update_savings_investments(request.user, when)
    metrics.update_retirement_investments(request.user, when)


def handle_transaction_update(request, transaction):
    rule = utils.create_categorisation_rule(request, transaction)
    transactions = queries.get_uncategorized_user_transactions(request)
    utils.apply_rule_to_transactions(rule, transactions)


def handle_rule_creation(request):
    rule = queries.insert_categorization_rule(request)
    utils.apply_rule_to_users_transactions(rule, request.user)

def handle_investment_input(request):
    account = queries.account_from_request(request)
    price = float(request.POST['price_in_CLP'])
    amount = float(request.POST['amount_in_account_CURRENCY'])
    date = request.POST['date']
    is_income = request.POST.get('is_income', False)
    description = "Invest_{}_for_{}_on_{}_to_{}".format(amount,
                                                        price,
                                                        date,
                                                        account.name)
    rate = price / amount
    prev_amount = AccountValue.objects.filter(
            account=account, valued_at__lt=date
        ).order_by('-valued_at')
    if prev_amount:
        prev_amount = prev_amount[0].value
    else:
        prev_amount = 0
    print("previous amount", prev_amount)
    _add_account_value(user=request.user,
                       account=account,
                       value=round(prev_amount + amount, 2),
                       valued_at=date)
    _add_transaction(user=request.user,
                     account=account,
                     amount=price,
                     type='income' if is_income else 'neutral',
                     transaction_id=helpers.build_transaction_id(
                        {"date": datetime.strptime(date, "%Y-%m-%d"),
                         "description": description,
                         "amount": price, "user_id":request.user.id,
                         "account_id": account.id}, "investment"),
                     description=description,
                     date=date,
                     category_id=24 if is_income else 15,
                     data_file_id=51,
                     )



# Internal Module Functions


def _add_exchange_rate(**kwargs):
    try:
        ExchangeRate.objects.get_or_create(**kwargs)
        return True
    except IntegrityError:
        print("IntegrityError when adding exchange rate")
        print(kwargs)
        print("Ignore that")
        return False


def _add_transaction(**kwargs):
    try:
        Transaction.objects.create(**kwargs)
        return True
    except IntegrityError as e:
        print("IntegrityError in Transaction detected")
        print(kwargs)
        print("ignore that...")
        print(e)
        return False

def _add_account_value(**kwargs):
    try:
        AccountValue.objects.get_or_create(**kwargs)
        return True
    except IntegrityError as e:
        print("IntegrityError in AccountValue detected")
        print(kwargs)
        print("Ignore that...")
        print(e)
        return False


def _apply_rules_to_uncategorized_transactions(request):
    all_rules = queries.get_all_categorization_rules(request)
    for rule in all_rules:
        transactions = queries.get_uncategorized_user_transactions(request)
        if not transactions:
            return
        utils.apply_rule_to_transactions(rule, transactions)


def _save_transactions_from_file_to_db(filepath, account, user, file):
    base_repr = {"user_id": user.id, "account_id": account.id}
    defaults = {"data_file_id": file.id}
    transaction_data = parsers.parse_transaction_file(filepath, base_repr=base_repr)
    transactions_added = []
    transactions_old = []
    for datum in transaction_data:
        datum = extractors.transaction(datum)
        datum.update(defaults)
        if _add_transaction(**datum):
            transactions_added.append(datum)
        else:
            transactions_old.append(datum)
    return transactions_added, transactions_old


def _save_account_values_from_file_to_db(filepath, account, user, file):
    base_repr = {"user_id": user.id, "account_id": account.id}
    transaction_data = parsers.parse_transaction_file(filepath, base_repr=base_repr)
    for datum in transaction_data:
        acc_val = extractors.account_value(datum)
        if not acc_val:
            continue
        acc_val.update(base_repr)
        _add_account_value(**acc_val)


def _add_entry_to_uploaded_files_table(user, account, uploaded_at):
    entry = UploadedFile.objects.create(user_id=user.id,
                                        account_id=account.id,
                                        uploaded_at=uploaded_at)
    return entry


def _change_account_value_based_on_transactions(transactions,
                                                account,
                                                user):
    print("Updating Account Value")
    # find all account values AT MOMENT OR AFTER the transaction was done (usually empty)
    # find account value previous to moment transaction was done
    # create new account value at the moment transaction was done
    # apply change to all account values after the moment of the transaction that already existed

    # What if two transactions at same time?
    #   while account_value at same time already exists:
    #       add one second to new account_value time
    #   add account_value at shifted time
    pass
