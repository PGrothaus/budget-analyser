import copy
import hashlib
import json
import pytz
from datetime import datetime

from business_logic import helpers

timezone = pytz.timezone("Chile/Continental")

def parse_banco_edwards_ccte(jdata):
    return jdata["movimientos"]


def parse_banco_edwards_tc_national(jdata):
    return jdata["seccionOperaciones"]["transaccionesTarjetas"]


def parse_banco_edwards_tc_national_no_facturado(jdata):
    return jdata["listaMovNoFactur"]


def parse_bbva_ccte(jdata):
    return jdata["lstCartolaCtaCte"]["movimientos"]


def parse_transaction_banco_edwards_ccte(datum, base_repr):
    base_repr["description"] = _format_description(datum["descripcion"])
    base_repr["amount"] = datum["montoMovimiento"]
    base_repr["currency"] = "CLP"
    base_repr["type"] = _format_transaction_type(datum["tipo"])
    base_repr["date"] = _format_transaction_date(datum["fecha"])
    base_repr["transaction_id"] = _build_transaction_id(base_repr)
    return base_repr


def parse_transaction_banco_edwards_tc_national(datum, base_repr):
    if datum["fechaTransaccionString"] is None:
        return None
    base_repr["description"] = _format_description(datum["descripcion"])
    base_repr["amount"] = datum["montoTransaccion"]
    base_repr["currency"] = "CLP"
    base_repr["type"] = _format_transaction_type(datum["grupo"])
    base_repr["date"] = _format_transaction_date(datum["fechaTransaccionString"], fix_time_of_day=True)
    base_repr["transaction_id"] = _build_transaction_id(base_repr)
    return base_repr


def parse_transaction_banco_edwards_tc_national_no_facturado(datum, base_repr):
    if datum["fechaTransaccionString"] is None:
        return None
    base_repr["description"] = _format_description(datum["glosaTransaccion"])
    base_repr["amount"] = datum["montoCompra"]
    base_repr["currency"] = "CLP"
    base_repr["type"] = "expense"
    base_repr["date"] = _format_transaction_date(" ".join([datum["fechaTransaccionString"], datum["horaAutorizacion"]]), fix_time_of_day=True)
    base_repr["transaction_id"] = _build_transaction_id(base_repr)
    return base_repr


def parse_transaction_bbva_ccte(datum, base_repr):
    base_repr["description"] = _format_description(datum["glosa"])
    base_repr["amount"] = _format_amount(datum["montomovfmt"])
    base_repr["currency"] = "CLP"
    base_repr["type"] = _format_transaction_type(datum["tipomov"])
    base_repr["date"] = _format_transaction_date(datum["fecmovfmt"])
    base_repr["transaction_id"] = _build_transaction_id(base_repr, datum["numdoc"])
    return base_repr

AVAILABLE_FILE_PARSERS = {
    "banco_edwards_ccte": parse_banco_edwards_ccte,
    "banco_edwards_tc_national": parse_banco_edwards_tc_national,
    "banco_edwards_tc_national_no_facturado": parse_banco_edwards_tc_national_no_facturado,
#    "banco_edwards_tc_international": parse_banco_edwards_tc_international,
    "bbva_ccte": parse_bbva_ccte,
}


AVAILABLE_TRANSACTION_PARSERS = {
    "banco_edwards_ccte": parse_transaction_banco_edwards_ccte,
    "banco_edwards_tc_national": parse_transaction_banco_edwards_tc_national,
    "banco_edwards_tc_national_no_facturado": parse_transaction_banco_edwards_tc_national_no_facturado,
#    "banco_edwards_tc_international": parse_transaction_banco_edwards_tc_international,
    "bbva_ccte": parse_transaction_bbva_ccte,
}


def parse_transaction_file(fp, base_repr=None):
    base_repr = {} if base_repr is None else base_repr
    jdata = load_json_data(fp)
    file_key = determine_file_key(jdata)
    transactions_data = _extract_transactions(jdata, file_key)
    for datum in transactions_data:
        base_repr_copy = copy.deepcopy(base_repr)
        trans = _format_transaction_datum(datum, file_key, base_repr_copy)
        if trans:
            yield trans


def load_json_data(filepath):
    with open(filepath, "r") as f:
        return json.load(f)


def determine_file_key(jdata):
    if jdata.get("movimientos") is not None:
        return "banco_edwards_ccte"
    elif jdata.get("seccionOperaciones") is not None:
        return "banco_edwards_tc_national"
    elif jdata.get("listaMovNoFactur") is not None:
        return "banco_edwards_tc_national_no_facturado"
    elif jdata.get("lstCartolaCtaCte") is not None:
        return "bbva_ccte"
    else:
        None


def _format_transaction_date(dateinfo, fix_time_of_day=False):
    elems = dateinfo.split(" ")
    if len(elems) == 1:
        date = elems[0]
        day, month, year = date.split("/")
        date = "".join([year, month, day])
        time = "12:00:00"
    elif len(elems) == 2:
        date, time = elems
        if "/" in date:
            day, month, year = date.split("/")
            date = "".join([year, month, day])
    else:
        raise ValueError("Unexpected datetime format in transaction.")
    if fix_time_of_day:
        time = "12:00:00"
    date = "{}-{}-{}".format(date[:4], date[4:6], date[6:])
    return timezone.localize(datetime.strptime(" ".join([date, time]), "%Y-%m-%d %H:%M:%S")).astimezone(pytz.utc)


def _format_amount(amount):
    amount = amount.replace(".", "")
    return int(amount)


def _build_transaction_id(datum, *args):
    key = helpers.datetime_to_integer(datum["date"])
    key += _hash_text(datum["description"])
    key += _hash_text(str(datum["amount"]))
    for arg in args:
        key += _hash_text(str(arg))
    idx = "{}{}{}".format(datum["user_id"], datum["account_id"], key)
    return int(idx)


def _format_transaction_type(type):
    type_formats = {"cargo": "expense",
                    "abono": "income",
                    "pagos": "expense",
                    "avancesCompras": "expense",
                    "A": "income",
                    "B": "expense",
                    "C": "expense",
                    }
    return type_formats[type]


def _format_transaction_datum(datum, file_key, base_repr):
    return AVAILABLE_TRANSACTION_PARSERS[file_key](datum, base_repr)


def _format_description(description):
    description = " ".join(description.split())
    description = description.lower()
    description = description.capitalize()
    return description


def _extract_transactions(data, file_key):
    return AVAILABLE_FILE_PARSERS[file_key](data)


def _hash_text(text):
    return int(hashlib.sha256(text.encode('utf-8')).hexdigest(), 16) % 10**8
