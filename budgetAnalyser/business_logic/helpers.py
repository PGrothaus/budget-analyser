import hashlib
import json
import os

from json_logic import jsonLogic

from api.serializers import TransactionSerializer
from backend import models


def exchange(amount, origin, target, when):
    if origin == target:
        return amount
    rates = (
        models.ExchangeRate.objects.filter(target__code=target, valued_at__lte=when,)
        .order_by("origin__code", "target__code", "-valued_at")
        .distinct("origin__code", "target__code")
    )
    rate = [elem.rate for elem in rates if elem.origin.code == origin][0]
    return amount * rate


def filepath_to_store_uploaded_transaction(user, bank, account, uploaded_at):
    dir = os.path.join(
        "/tmp/user_data/",
        str(user.id),
        bank.name,
        account.name,
        "uploaded_transaction_files",
    )
    filename = "{}.json".format(uploaded_at)
    return _format_filepath(os.path.join(dir, filename))


def _format_filepath(filepath):
    filepath = filepath.replace(" ", "_")
    filepath = filepath.replace("+00:00.json", ".json")
    return filepath


def rule_is_fulfilled(rule, transaction):
    transaction_json = TransactionSerializer(transaction).data
    rule_json = json.loads(rule.rule)
    res = jsonLogic(rule_json, {"transaction": transaction_json})
    return res is True  # NOTE: Needed to return False if rule is invalid


def build_transaction_id(datum, *args):
    key = datetime_to_integer(datum["date"])
    key += _hash_text(datum["description"])
    key += _hash_text(str(datum["amount"]))
    for arg in args:
        key += _hash_text(str(arg))
    idx = "{}{}{}".format(datum["user_id"], datum["account_id"], key)
    return int(idx)


def _hash_text(text):
    return int(hashlib.sha256(text.encode("utf-8")).hexdigest(), 16) % 10 ** 8


def datetime_to_integer(dt_time):
    return (
        10 ** 10 * dt_time.year
        + 10 ** 8 * dt_time.month
        + 10 ** 6 * dt_time.day
        + 10 ** 4 * dt_time.hour
        + 10 ** 2 * dt_time.minute
        + 10 ** 0 * dt_time.second
    )
