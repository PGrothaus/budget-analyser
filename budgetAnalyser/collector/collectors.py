import requests
import re
import time
from datetime import datetime
from backend import models



def collect_all():
    print("Collecting all")
    collect_value_uf()
    collect_values_planvital()
    collect_value_currencies()


def collect_value_currencies():
    for cur in ["EUR", "GBP", "USD"]:
        time.sleep(3)
        collect_rate_currency(cur)


def collect_rate_currency(cur):
    payload = {"Amount": 1, "From": cur, "To": "CLP"}
    pk = {"EUR": 3, "GBP": 4, "USD": 5}.get(cur)
    response = requests.get("https://transferwise.com/gb/currency-converter/{}-to-clp-rate".format(cur.lower()))
    value = extract_value_currency(response, cur)
    post_to_db(value, pk)



def collect_values_planvital():
    for fondo in ["A", "B", "C", "D", "E"]:
        collect_value_fondo(fondo)


def collect_value_fondo(fondo):
    payload = {"tf": fondo}
    response = requests.get("https://www.spensiones.cl/apps/valoresCuotaFondo/vcfAFP.php", params=payload)
    value = extract_value_fondo(response)
    post_value_fondo_to_db(value, fondo)


def collect_value_uf():
    value = get_value_uf()
    post_to_db(value, 2)


def get_value_uf():
    response = make_request_uf()
    return extract_value_uf(response)


def post_to_db(value, origin):
    payload = {"origin": origin,
               "target": 1,
               "rate": value,
               "valued_at": datetime.now()}
    models.ExchangeRate.objects.create(
        origin_id=origin,
        target_id=1,
        rate=value,
        valued_at=datetime.now()
    )
#    r = requests.post("http://127.0.0.1:8000/api/exchange_rate_add", data=payload)
#    if r.status_code != 201:
#        print(r.status_code)
#        print(r.text)
    print("Saved Rate to DB: {}-{}: {}".format(origin, "CLP", value))


def post_value_fondo_to_db(value, fondo):
    fondo_pk = {"A": 6, "B": 7, "C": 8, "D": 9, "E": 10}.get(fondo)
    post_to_db(value, fondo_pk)


def make_request_uf():
    return requests.get('https://valoruf.cl/')


def extract_value_uf(response):
    p = re.compile("<td class=\"text-right\">1</td><td class=\"text-right\">\d{1,3}.\d{1,4},\d{1,3}</td>")
    match = p.search(response.text).group(0)
    return extract_value_uf_from_match(match)


def extract_value_fondo(response):
    text = response.text.replace(" ", "").replace("\n", "")
    pttrn = "PLANVITAL</td><tdalign=\"right\">\d{1,3}.\d{1,4},\d{1,3}"
    p = re.compile(pttrn)
    match = p.search(text).group(0)
    return extract_value_fondo_from_match(match)


def extract_value_currency(response, cur):
    text = response.text.replace(" ", "")
    pttrn = "config.currentRate=\d{1,4}.\d{1,4}"
    p = re.compile(pttrn)
    match = p.search(text).group(0)
    return extract_value_currency_from_match(match)


def extract_value_uf_from_match(matched_pattern):
    uf_string = matched_pattern.split(">")[-2].split("<")[0]
    return float(uf_string.replace(".", "").replace(",", "."))


def extract_value_fondo_from_match(matched_pattern):
    value_string = matched_pattern.split(">")[-1]
    return float(value_string.replace(".", "").replace(",", "."))


def extract_value_currency_from_match(match):
    return float(match.split("=")[-1])


if "__main__" == __name__:
    collect_all()
