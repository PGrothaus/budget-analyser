from datetime import datetime
import pytz

from django.test import TestCase
from django.test import RequestFactory
from django.test import Client
from django.http import Http404
from django.contrib.auth.models import AnonymousUser

from backend import views
from backend.models import Account
from backend.models import Bank
from backend.models import Transaction
from backend.models import UploadedFile
from custom_auth.models import MyUser


class ATransactionDetailView(TestCase):

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
        self.account = Account.objects.create(
            name="test-account",
            bank=self.bank,
            user=self.user,
        )
        self.uploaded_file = UploadedFile.objects.create(
            user=self.user,
            account=self.account,
            uploaded_at=pytz.utc.localize(datetime.now()),
        )
        self.transaction = Transaction.objects.create(
            transaction_id=123123123123,
            description="test-transaction",
            amount=25000,
            currency="CLP",
            type="gasto",
            date=pytz.utc.localize(datetime.now()),
            account=self.account,
            user=self.user,
            data_file=self.uploaded_file,
        )
        self.other_user = MyUser.objects.create(
            email="user2@gmail.com",
            date_of_birth="2000-01-02",
        )
        self.other_user.set_password('abc')
        self.other_user.save()

        self.pk_transaction = Transaction.objects.get(
            transaction_id=self.transaction.transaction_id).pk
        self.client = Client()

    def test_can_show_transaction_to_its_user(self):
        self.client.login(email="user@gmail.com", password='abc')
        response = self.client.get('/transactions/{}'.format(self.pk_transaction))
        assert self.transaction == response.context['transaction']

    def test_shows_404_for_nonexisting_transaction(self):
        self.client.login(email="user@gmail.com", password='abc')
        response = self.client.get('/transactions/{}'.format(self.pk_transaction + 25))
        assert 404 == response.status_code
        assert 'transaction' not in response.context

    def test_does_not_show_transaction_to_another_user(self):
        self.client.login(email="user2@gmail.com", password='abc')
        response = self.client.get('/transactions/{}'.format(self.pk_transaction))
        assert 404 == response.status_code
        assert 'transaction' not in response.context


    def test_does_not_show_transaction_to_anonymous_user(self):
        response = self.client.get('/transactions/{}'.format(self.pk_transaction))
        assert 302 == response.status_code
        assert response.context is None


class ATransactionListView(TestCase):

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
        self.account = Account.objects.create(
            name="test-account",
            bank=self.bank,
            user=self.user,
        )
        self.uploaded_file = UploadedFile.objects.create(
            user=self.user,
            account=self.account,
            uploaded_at=pytz.utc.localize(datetime.now()),
        )
        self.transactions = []
        self.transactions.append(Transaction.objects.create(
            transaction_id=123123123123,
            description="test-transaction",
            amount=25000,
            currency="CLP",
            type="expense",
            date=pytz.utc.localize(datetime.now()),
            account=self.account,
            user=self.user,
            data_file=self.uploaded_file,
        ))
        self.transactions.append(Transaction.objects.create(
            transaction_id=123123123124,
            description="test-transaction",
            amount=52000,
            currency="CLP",
            type="income",
            date=pytz.utc.localize(datetime.now()),
            account=self.account,
            user=self.user,
            data_file=self.uploaded_file,
        ))
        self.other_user = MyUser.objects.create(
            email="user2@gmail.com",
            date_of_birth="2000-01-02",
        )
        self.other_user.set_password('abc')
        self.other_user.save()

        self.client = Client()

    def test_can_show_transaction_list_to_its_user(self):
        self.client.login(email="user@gmail.com", password='abc')
        response = self.client.get('/transactions')
        assert self.transactions[0] in response.context['transaction_list']
        assert self.transactions[1] in response.context['transaction_list']
        assert len(response.context['transaction_list']) == 2

    def test_shows_empty_transaction_list_to_another_user(self):
        self.client.login(email="user2@gmail.com", password='abc')
        response = self.client.get('/transactions')
        assert len(response.context['transaction_list']) == 0


    def test_does_not_show_transactions_list_to_anonymous_user(self):
        response = self.client.get('/transactions')
        assert 302 == response.status_code
        assert response.context is None
