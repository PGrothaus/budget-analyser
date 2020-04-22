import yaml

from lib import Transaction


def edit_transactions(transactions):
    edits = _load_transaction_edits()
    transactions_edited = _apply_edits(transactions, edits)
    return transactions_edited


def _apply_edits(transactions, edits):
    transactions_edited = []
    for i, trans in enumerate(transactions):
        if trans.id not in edits:
            transactions_edited.append(trans)
            continue
        trans_new = trans._asdict()
        trans_new.update(edits[trans.id])
        trans_new = Transaction(**trans_new)
        transactions_edited.append(trans_new)
        print("INFO: Transaction updated", trans_new)
    return transactions_edited


def _load_transaction_edits():
    data = _load_raw_data()
    return {datum["id"]: datum for datum in data}


def _load_raw_data():
    fp = "./data/transaction_edits.yaml"
    with open(fp, "r") as f:
        return yaml.load(f, Loader=yaml.FullLoader)
