import datetime
import json
import unittest
import pytz

from business_logic import parsers


timezone = pytz.timezone("Chile/Continental")


class BancoEdwardsCCTEParsingTestCase(unittest.TestCase):

    def setUp(self):
        fp = "backend/tests/data/transactions.banco_edwards.json"
        base_repr = {"user_id": 1, "account_id": 2}
        self.transactions = parsers.parse_transaction_file(fp, base_repr=base_repr)

    def test_returns_two_data_entries(self):
        assert len(list(self.transactions)) == 2

    def test_first_transaction_has_correct_user_id(self):
        trans = list(self.transactions)[0]
        assert trans["user_id"] == 1

    def test_first_transaction_has_correct_account_id(self):
        trans = list(self.transactions)[0]
        assert trans["account_id"] == 2

    def test_first_transaction_has_correct_transaction_id(self):
        trans = list(self.transactions)[0]
        print(trans["transaction_id"])
        assert trans["transaction_id"] == 1220200536420184

    def test_first_transaction_has_correct_description(self):
        trans = list(self.transactions)[0]
        assert trans["description"] == "Pago en previred.com*"

    def test_first_transaction_has_correct_amount(self):
        trans = list(self.transactions)[0]
        assert trans["amount"] == 1000

    def test_first_transaction_has_correct_currency(self):
        trans = list(self.transactions)[0]
        assert trans["currency"] == "CLP"

    def test_first_transaction_has_correct_date(self):
        trans = list(self.transactions)[0]
        assert trans["date"] == timezone.localize(datetime.datetime(2020, 4, 15, 16, 54, 11)).astimezone(pytz.utc)

    def test_second_transaction_has_correct_user_id(self):
        trans = list(self.transactions)[1]
        assert trans["user_id"] == 1

    def test_second_transaction_has_correct_account_id(self):
        trans = list(self.transactions)[1]
        assert trans["account_id"] == 2

    def test_second_transaction_has_correct_transaction_id(self):
        trans = list(self.transactions)[1]
        print("parsing ccte", trans["transaction_id"])
        assert trans["transaction_id"] == 1220200543416050

    def test_second_transaction_has_correct_description(self):
        trans = list(self.transactions)[1]
        assert trans["description"] == "Pac metrogas sa"

    def test_second_transaction_has_correct_amount(self):
        trans = list(self.transactions)[1]
        assert trans["amount"] == 2000

    def test_second_transaction_has_correct_currency(self):
        trans = list(self.transactions)[1]
        assert trans["currency"] == "CLP"

    def test_second_transaction_has_correct_date(self):
        trans = list(self.transactions)[1]
        assert trans["date"] == timezone.localize(datetime.datetime(2020, 4, 14, 1, 24, 49)).astimezone(pytz.utc)


class BancoEdwardsTCNationalParsingTestCase(unittest.TestCase):

    def setUp(self):
        fp = "backend/tests/data/transactions.banco_edwards.tc_national.json"
        base_repr = {"user_id": 1, "account_id": 2}
        self.transactions = parsers.parse_transaction_file(fp, base_repr=base_repr)

    def test_returns_two_data_entries(self):
        assert len(list(self.transactions)) == 3

    def test_returns_first_transaction_correctly(self):
        expected = {
            "user_id": 1,
            "account_id": 2,
            "transaction_id": 1220200518967844,
            "description": "Fruterra",
            "amount": 1234.0,
            "currency": "CLP",
            "type": "expense",
            "date": timezone.localize(datetime.datetime(2020, 4, 21, 12, 0, 0)).astimezone(pytz.utc),
        }
        trans = list(self.transactions)[0]
        print("parsing tc national 1", trans["transaction_id"])
        assert trans == expected

    def test_returns_second_transaction_correctly(self):
        expected = {
            "user_id": 1,
            "account_id": 2,
            "transaction_id": 1220200398858661,
            "description": "Hdi seguros pat compras",
            "amount": 10000,
            "currency": "CLP",
            "type": "expense",
            "date": timezone.localize(datetime.datetime(2020, 3, 26, 12, 0, 0)).astimezone(pytz.utc),
        }
        trans = list(self.transactions)[1]
        print("parsing tc national 2", trans["transaction_id"])
        assert trans == expected


class BancoEdwardsTCNoFacturadoParsingTestCase(unittest.TestCase):

    def setUp(self):
        fp = "backend/tests/data/transactions.tc.no_facturado.json"
        base_repr = {"user_id": 1, "account_id": 2}
        self.transactions = parsers.parse_transaction_file(fp, base_repr=base_repr)

    def test_returns_two_data_entries(self):
        assert len(list(self.transactions)) == 2

    def test_first_transaction_has_correct_user_id(self):
        trans = list(self.transactions)[0]
        assert trans["user_id"] == 1

    def test_first_transaction_has_correct_account_id(self):
        trans = list(self.transactions)[0]
        assert trans["account_id"] == 2

    def test_first_transaction_has_correct_transaction_id(self):
        trans = list(self.transactions)[0]
        print("parsing tc no facturado", trans["transaction_id"])
        assert trans["transaction_id"] == 1220200514878615

    def test_first_transaction_has_correct_description(self):
        trans = list(self.transactions)[0]
        assert trans["description"] == "Ekono los leones ii compras"

    def test_first_transaction_has_correct_amount(self):
        trans = list(self.transactions)[0]
        assert trans["amount"] == 3424

    def test_first_transaction_has_correct_currency(self):
        trans = list(self.transactions)[0]
        assert trans["currency"] == "CLP"

    def test_first_transaction_has_correct_date(self):
        trans = list(self.transactions)[0]
        print("parsing tc non facturado", trans["date"])
        assert trans["date"] == timezone.localize(datetime.datetime(2020, 4, 30, 12, 0, 0)).astimezone(pytz.utc)

    def test_second_transaction_has_correct_user_id(self):
        trans = list(self.transactions)[1]
        assert trans["user_id"] == 1

    def test_second_transaction_has_correct_account_id(self):
        trans = list(self.transactions)[1]
        assert trans["account_id"] == 2

    def test_second_transaction_has_correct_transaction_id(self):
        trans = list(self.transactions)[1]
        print(trans["transaction_id"])
        assert trans["transaction_id"] == 1220200484757658

    def test_second_transaction_has_correct_description(self):
        trans = list(self.transactions)[1]
        assert trans["description"] == "Almacen salinas facco compras"

    def test_second_transaction_has_correct_amount(self):
        trans = list(self.transactions)[1]
        assert trans["amount"] == 1550

    def test_second_transaction_has_correct_currency(self):
        trans = list(self.transactions)[1]
        assert trans["currency"] == "CLP"

    def test_second_transaction_has_correct_date(self):
        trans = list(self.transactions)[1]
        print(trans["date"])
        assert trans["date"] == timezone.localize(datetime.datetime(2020, 4, 30, 12, 0, 0)).astimezone(pytz.utc)


class ScotiabankCCTEParsingTestCase(unittest.TestCase):

    def setUp(self):
        fp = "backend/tests/data/transactions.scotiabank.json"
        base_repr = {"user_id": 1, "account_id": 2}
        self.transactions = parsers.parse_transaction_file(fp, base_repr=base_repr)

    def test_returns_two_data_entries(self):
        assert len(list(self.transactions)) == 2

    def test_first_transaction_has_correct_user_id(self):
        trans = list(self.transactions)[0]
        assert trans["user_id"] == 1

    def test_first_transaction_has_correct_account_id(self):
        trans = list(self.transactions)[0]
        assert trans["account_id"] == 2

    def test_first_transaction_has_correct_transaction_id(self):
        trans = list(self.transactions)[0]
        print("parsing scotiabank 1", trans["transaction_id"])
        assert trans["transaction_id"] == 1220200320248606

    def test_first_transaction_has_correct_description(self):
        trans = list(self.transactions)[0]
        assert trans["description"] == "Compra"

    def test_first_transaction_has_correct_amount(self):
        trans = list(self.transactions)[0]
        assert trans["amount"] == 10000

    def test_second_transaction_has_correct_type(self):
        trans = list(self.transactions)[0]
        assert trans["type"] == "expense"

    def test_first_transaction_has_correct_currency(self):
        trans = list(self.transactions)[0]
        assert trans["currency"] == "CLP"

    def test_first_transaction_has_correct_date(self):
        trans = list(self.transactions)[0]
        assert trans["date"] == timezone.localize(datetime.datetime(2020, 1, 28, 12, 0, 0)).astimezone(pytz.utc)

    def test_second_transaction_has_correct_user_id(self):
        trans = list(self.transactions)[1]
        assert trans["user_id"] == 1

    def test_second_transaction_has_correct_account_id(self):
        trans = list(self.transactions)[1]
        assert trans["account_id"] == 2

    def test_second_transaction_has_correct_transaction_id(self):
        trans = list(self.transactions)[1]
        print("parsing scotiabank 2", trans["transaction_id"])
        assert trans["transaction_id"] == 1220200338855752

    def test_second_transaction_has_correct_description(self):
        trans = list(self.transactions)[1]
        assert trans["description"] == "Abono"

    def test_second_transaction_has_correct_amount(self):
        trans = list(self.transactions)[1]
        assert trans["amount"] == 17370

    def test_second_transaction_has_correct_currency(self):
        trans = list(self.transactions)[1]
        assert trans["currency"] == "CLP"

    def test_second_transaction_has_correct_type(self):
        trans = list(self.transactions)[1]
        assert trans["type"] == "income"

    def test_second_transaction_has_correct_date(self):
        trans = list(self.transactions)[1]
        assert trans["date"] == timezone.localize(datetime.datetime(2020, 1, 28, 12, 0, 0)).astimezone(pytz.utc)
