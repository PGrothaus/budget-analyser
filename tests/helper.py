import json


def load_transaction_data():
    fp = "./tests/data/transactions.json"
    with open(fp, "r") as f:
        return json.load(f)
