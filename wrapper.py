from tests import helper
from lib import parsers
from lib import categoriser
from lib import editors


data = helper.load_transaction_data()
transactions = parsers.parse_transactions_data(data)
transactions = editors.edit_transactions(transactions)
cats = categoriser.categorise_transactions(transactions)
_, groups, subgroups = zip(* cats)

grouped = {}
for cat in cats:
    trans, group, subgroup = cat
    if group not in grouped:
        grouped[group] = 0
    grouped[group] += trans.montoMovimiento

print(grouped)
