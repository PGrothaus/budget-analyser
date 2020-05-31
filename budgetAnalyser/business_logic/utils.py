import json
import os
from datetime import datetime

from business_logic import helpers
from backend.models import Category
from backend.models import Transaction
from rule_system.models import CategorizationRule


def apply_rule_to_users_transactions(rule, user):
    transactions_user = Transaction.objects.filter(user=user)
    apply_rule_to_transactions(rule, transactions_user)


def apply_rule_to_transactions(rule, transactions):
    category = Category.objects.get(pk=rule.effect_value.pk)
    for transaction in transactions:
        apply_rule_to_single_transaction(transaction, rule, category)


def apply_rule_to_single_transaction(transaction, rule, category):
    if helpers.rule_is_fulfilled(rule, transaction):
        print("Update Category of Transaction")
        transaction.category = category
        transaction.save()


def create_categorisation_rule(request, transaction):
    cat = transaction.category
    description = transaction.description
    rule = {"==": [{"var": "transaction.description"}, description]}
    jdata = json.dumps(rule)
    date = str(helpers.datetime_to_integer(datetime.now()))
    name = "{}:{}".format(cat.name, date)
    return CategorizationRule.objects.create(name=name,
                                             rule=jdata,
                                             user=request.user,
                                             effect_value=cat)


def create_missing_dirs(filepath):
    dir = os.path.dirname(filepath)
    if not os.path.isdir(dir):
        print("Create directory at", dir)
        os.makedirs(dir)


def save_uploaded_file(filepath, file):
    create_missing_dirs(filepath)
    with open(filepath, 'wb+') as destination:
        print("Save uploaded file at", filepath)
        for chunk in file.chunks():
            destination.write(chunk)
