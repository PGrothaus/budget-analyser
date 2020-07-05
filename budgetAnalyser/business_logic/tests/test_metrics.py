from django.test import TestCase
from django.test import Client

import pytz
from datetime import datetime

from business_logic import metrics
from backend import views
from backend.models import Bank
from backend.models import Account
from backend.models import AccountValue
from backend.models import AccountType
from backend.models import Currency
from backend.models import ExchangeRate
from backend.models import Transaction
from backend.models import UploadedFile
from custom_auth.models import MyUser

class GetSavingAccountValues(TestCase):

    def setUp(self):
        self.user = MyUser.objects.create(
            email="user@gmail.com",
            date_of_birth="2000-01-01",
        )
        self.user.set_password('abc')
        self.user.save()

        self.bank = Bank.objects.create(
            name="test-bank",
            user=self.user,
        )
        self.account_type = AccountType.objects.create(
            type="NORMAL"
        )
        self.account = Account.objects.create(
            name="test-account",
            bank=self.bank,
            user=self.user,
            type=self.account_type
        )
        self.accVal1 = AccountValue.objects.create(
            user=self.user,
            account=self.account,
            value=100,
            valued_at=pytz.utc.localize(datetime(2020, 7, 2, 14, 0, 0))
        )
        self.accVal2 = AccountValue.objects.create(
            user=self.user,
            account=self.account,
            value=200,
            valued_at=pytz.utc.localize(datetime(2020, 7, 2, 15, 0, 0))
        )
        self.client = Client()

    def test_returns_the_most_recent_value_as_default(self):
        self.client.login(email="user@gmail.com", password='abc')
        res = metrics.get_savings_account_values(self.user)
        assert res[0] == self.accVal2

    def test_returns_the_closest_value_when_provided_a_when(self):
        self.client.login(email="user@gmail.com", password='abc')
        res = metrics.get_savings_account_values(
            self.user,
            when=pytz.utc.localize(datetime(2020, 7, 2, 14, 30, 0)),
        )
        assert res[0] == self.accVal1

    def test_returns_empty_qset_value_when__no_values_exists(self):
        self.client.login(email="user@gmail.com", password='abc')
        res = metrics.get_savings_account_values(
            self.user,
            when=datetime(2010, 7, 2, 14, 30, 0),
        )
        assert len(res) == 0


class TotalSavingTestCase(TestCase):

    def setUp(self):
        self.user = MyUser.objects.create(
            email="user@gmail.com",
            date_of_birth="2000-01-01",
        )
        self.user.set_password('abc')
        self.user.save()

        self.bank = Bank.objects.create(
            name="test-bank",
            user=self.user,
        )
        self.account_type = AccountType.objects.create(
            type="NORMAL"
        )
        self.rate1 = ExchangeRate.objects.create(
            origin=Currency.objects.get(code="USD"),
            target=Currency.objects.get(code="CLP"),
            rate=800,
            valued_at=pytz.utc.localize(datetime(2020, 7, 2, 14, 0, 0))
        )
        self.rate2 = ExchangeRate.objects.create(
            origin=Currency.objects.get(code="USD"),
            target=Currency.objects.get(code="CLP"),
            rate=100,
            valued_at=pytz.utc.localize(datetime(2020, 7, 2, 15, 0, 0))
        )
        self.account1 = Account.objects.create(
            name="test-account",
            bank=self.bank,
            user=self.user,
            type=self.account_type,
            currency=Currency.objects.get(code="USD")
        )
        self.accVal1 = AccountValue.objects.create(
            user=self.user,
            account=self.account1,
            value=100,
            valued_at=pytz.utc.localize(datetime(2020, 7, 2, 14, 0, 0))
        )
        self.accVal2 = AccountValue.objects.create(
            user=self.user,
            account=self.account1,
            value=200,
            valued_at=pytz.utc.localize(datetime(2020, 7, 2, 15, 0, 0))
        )
        self.account2 = Account.objects.create(
            name="other-test-account",
            bank=self.bank,
            user=self.user,
            type=self.account_type,
            currency=Currency.objects.get(code="USD")
        )
        self.accVal3 = AccountValue.objects.create(
            user=self.user,
            account=self.account2,
            value=1000,
            valued_at=pytz.utc.localize(datetime(2020, 7, 2, 14, 0, 0))
        )
        self.accVal4 = AccountValue.objects.create(
            user=self.user,
            account=self.account2,
            value=2000,
            valued_at=pytz.utc.localize(datetime(2020, 7, 2, 15, 0, 0))
        )
        self.client = Client()

    def test_returns_the_most_recent_total_as_default(self):
        self.client.login(email="user@gmail.com", password='abc')
        res = metrics.savings(self.user, to_currency="USD")
        assert res == 2200

    def test_returns_the_closest_total_when_a_date_is_provided(self):
        self.client.login(email="user@gmail.com", password='abc')
        res = metrics.savings(
            self.user,
            when=pytz.utc.localize(datetime(2020, 7, 2, 14, 30, 0)),
            to_currency="USD"
        )
        assert res == 1100

    def test_returns_the_most_recent_total_in_correct_currency_as_default(self):
        self.client.login(email="user@gmail.com", password='abc')
        res = metrics.savings(self.user, to_currency="CLP")
        assert res == 2200 * 100

    def test_returns_the_closest_total_in_correct_currency_when_a_date_is_provided(self):
        self.client.login(email="user@gmail.com", password='abc')
        res = metrics.savings(
            self.user,
            when=pytz.utc.localize(datetime(2020, 7, 2, 14, 30, 0)),
            to_currency="CLP"
        )
        assert res == 1100 * 800
