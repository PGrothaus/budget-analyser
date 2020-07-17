import os
import shutil
import time

from django.contrib.auth.models import AnonymousUser
from django.http import Http404
from django.test import TestCase
from django.test import RequestFactory
from django.test import Client

from backend import views
from backend.models import Bank
from backend.models import Account
from backend.models import Transaction
from backend.models import UploadedFile
from custom_auth.models import MyUser


class APostTransactionsBancoEdwardsCCTEUploadView(TestCase):

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
            type_id=2,
        )

        self.other_user = MyUser.objects.create(
            email="user2@gmail.com",
            date_of_birth="2000-01-02",
        )
        self.other_user.set_password('abc')
        self.other_user.save()

        self.client = Client(follow=True)
        self.fp_transactions = "./backend/tests/data/transactions.banco_edwards.json"

        self.client.login(email="user@gmail.com", password='abc')


    def _upload_transactions(self):
        """Make a post request to upload a json file containing transactions.

        Note that this method runs asynchronously.
        """
        with open(self.fp_transactions) as fp:
            self.response = self.client.post('/transactions/upload', {
                'file': fp,
                'bank': self.bank.pk,
                'account': self.account.pk,
                }
            )

    def tearDown(self):
        try:
            shutil.rmtree("/tmp/user_data/")
        except:
            pass

    def test_entry_added_to_uploaded_files_table(self):
        self._upload_transactions()
        elems = UploadedFile.objects.filter(user=self.user,
                                            account=self.account)
        assert len(elems) == 1

    def test_file_was_stored_at_the_correct_filepath(self):
        self._upload_transactions()
        dir = "/tmp/user_data/{}/{}/{}/uploaded_transaction_files/".format(
            self.user.id, self.bank.name, self.account.name)
        files = os.listdir(dir)
        assert len(files) == 1

    def test_transactions_have_correct_amount(self):
        self._upload_transactions()
        elems = Transaction.objects.filter(user_id=self.user.id)
        assert [1000, 2000] == sorted([elem.amount for elem in elems])

    def test_ignores_a_transaction_that_was_already_uploaded(self):
        self._upload_transactions()
        items = Transaction.objects.filter(user=self.user)
        assert len(items) == 2
        time.sleep(2)
        self._upload_transactions
        items = Transaction.objects.filter(user=self.user)
        assert len(items) == 2

    def test_user_cannot_add_transactions_to_other_users_account(self):
        self.client.logout()
        self.client.login(email="user2@gmail.com", password='abc')
        with open(self.fp_transactions) as fp:
            response = self.client.post('/transactions/upload',
                {'file': fp, 'account': self.account.pk, 'bank': self.bank.pk})
        items = Transaction.objects.filter(user=self.user)
        assert len(items) == 0

    def test_anonymous_user_cannot_add_transactions(self):
        self.client.logout()
        with open(self.fp_transactions) as fp:
            response = self.client.post('/transactions/upload',
                {'file': fp, 'account': self.account.pk, 'bank': self.bank.pk})
        assert 302 == response.status_code

    def test_redirects_to_transactions_upload(self):
        self._upload_transactions()
        self.assertRedirects(self.response, '/transactions/upload')


class APostTransactionsBancoEdwardsTCUploadView(TestCase):

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
            type_id=2,
        )

        self.client = Client(follow=True)
        self.client.login(email="user@gmail.com", password='abc')
        self.fp_transactions = "./backend/tests/data/transactions.banco_edwards.tc_national.json"


    def _upload_transactions(self):
        with open(self.fp_transactions) as fp:
            self.response = self.client.post('/transactions/upload', {
                'file': fp,
                'bank': self.bank.pk,
                'account': self.account.pk,
                }
            )

    def tearDown(self):
        try:
            shutil.rmtree("/tmp/user_data/")
        except:
            pass

    def test_entry_added_to_uploaded_files_table(self):
        self._upload_transactions()
        elems = UploadedFile.objects.filter(user=self.user,
                                            account=self.account)
        assert len(elems) == 1

    def test_file_was_stored_at_the_correct_filepath(self):
        self._upload_transactions()
        dir = "/tmp/user_data/{}/{}/{}/uploaded_transaction_files/".format(
            self.user.id, self.bank.name, self.account.name)
        files = os.listdir(dir)
        assert len(files) == 1

    def test_can_upload_transactions_of_same_day(self):
        self._upload_transactions()
        elems = Transaction.objects.filter(user_id=self.user.id)
        assert len(elems) == 3

    def test_transactions_have_correct_amount(self):
        self._upload_transactions()
        elems = Transaction.objects.filter(user_id=self.user.id)
        assert [1234, 10000, 20000] == sorted([elem.amount for elem in elems])
