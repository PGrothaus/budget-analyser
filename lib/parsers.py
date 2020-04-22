from lib import Transaction


def parse_transactions_data(data):
    transactions = data["JSON"]["movimientos"]
    transactions = [_parse_transaction(datum) for datum in transactions]
    return transactions


def _parse_transaction(datum):
    return Transaction(**datum)
