

def account_value(datum):
    value = datum.get("new_account_value")
    if not value:
        return None
    else:
        return {"valued_at": datum["date"],
                "value": value}


def transaction(datum):
    keys = ["description",
            "amount",
            "currency",
            "type",
            "date",
            "transaction_id",
            "user_id",
            "account_id",
            ]
    return {key: datum[key] for key in keys}
