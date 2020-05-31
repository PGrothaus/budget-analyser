import pytz
from datetime import datetime

from django.db import IntegrityError

from . import helpers
from . import parsers
from . import queries
from . import utils
from backend.models import Transaction
from backend.models import UploadedFile


def handle_transactions_upload(request):
    bank = queries.bank_from_request(request)
    account = queries.account_from_request(request, bank)
    uploaded_at = pytz.utc.localize(datetime.now())
    filepath = helpers.filepath_to_store_uploaded_transaction(
        request.user, bank, account, uploaded_at)
    entry_file = _add_entry_to_uploaded_files_table(
        request.user, account, uploaded_at)
    utils.save_uploaded_file(filepath, request.FILES['file'])
    _save_transactions_from_file_to_db(
        filepath, account, request.user, entry_file)
    _apply_rules_to_uncategorized_transactions(request)


def handle_transaction_update(request, transaction):
    rule = utils.create_categorisation_rule(request, transaction)
    transactions = queries.get_uncategorized_user_transactions(request)
    utils.apply_rule_to_transactions(rule, transactions)


def handle_rule_creation(request):
    rule = queries.insert_categorization_rule(request)
    utils.apply_rule_to_users_transactions(rule, request.user)


# Internal Module Functions


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
    for datum in transaction_data:
        datum.update(defaults)
        try:
            Transaction.objects.create(**datum)
        except IntegrityError:
            print("IntegrityError detected")
            print(datum)
            print("ignore that...")
            pass


def _add_entry_to_uploaded_files_table(user, account, uploaded_at):
    entry = UploadedFile.objects.create(user_id=user.id,
                                        account_id=account.id,
                                        uploaded_at=uploaded_at)
    return entry
