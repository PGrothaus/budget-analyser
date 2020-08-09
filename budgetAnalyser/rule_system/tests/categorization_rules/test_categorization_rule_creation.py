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
from rule_system.models import CategorizationRule
from backend.models import Category
from backend.models import CategoryGroup
from backend.models import Transaction
from backend.models import UploadedFile
from custom_auth.models import MyUser


class ACategorisationRuleCreationView(TestCase):
    def setUp(self):
        self.user = MyUser.objects.create(
            email="user@gmail.com", date_of_birth="2000-01-01",
        )
        self.user.set_password("abc")
        self.user.save()
        self.category_group = CategoryGroup.objects.create(
            name="Essentials", type="expense"
        )
        self.category = Category.objects.create(
            name="Groceries", group=self.category_group
        )
        self.bank = Bank.objects.create(name="test-bank", user=self.user,)
        self.account = Account.objects.create(
            name="test-account", bank=self.bank, user=self.user, type_id=2,
        )
        self.uploaded_file = UploadedFile.objects.create(
            user=self.user,
            account=self.account,
            uploaded_at=pytz.utc.localize(datetime.now()),
        )
        self.transactions = []
        self.transactions.append(
            Transaction.objects.create(
                transaction_id=123123123123,
                description="food",
                amount=25000,
                currency="CLP",
                type="expense",
                date=pytz.utc.localize(datetime.now()),
                account=self.account,
                user=self.user,
                data_file=self.uploaded_file,
            )
        )
        self.transactions.append(
            Transaction.objects.create(
                transaction_id=123123123124,
                description="drink",
                amount=52000,
                currency="CLP",
                type="expense",
                date=pytz.utc.localize(datetime.now()),
                account=self.account,
                user=self.user,
                data_file=self.uploaded_file,
            )
        )
        self.other_user = MyUser.objects.create(
            email="user2@gmail.com", date_of_birth="2000-01-02",
        )
        self.other_user.set_password("abc")
        self.other_user.save()

        self.client = Client()
        self.client.login(email="user@gmail.com", password="abc")
        self.response = self.client.post(
            "/rules/categorization/create",
            {
                "name": "test-rule",
                "rule": '{"==": [{"var": "transaction.description"}, "food"]}',
                "effect_value": self.category.id,
            },
        )

    def test_can_add_a_rule_to_the_users_rules(self):
        elems = CategorizationRule.objects.filter(user=self.user)
        assert len(elems) == 1

    def test_cannot_add_a_rule_to_other_users_rules(self):
        elems = CategorizationRule.objects.filter(user=self.other_user)
        assert len(elems) == 0

    def test_the_rule_is_correctly_applied_to_the_food_transaction(self):
        transaction = Transaction.objects.get(pk=self.transactions[0].pk)
        assert transaction.category == self.category

    def test_the_rule_was_not_applied_to_the_drink_transaction(self):
        transaction = Transaction.objects.get(pk=self.transactions[1].pk)
        print(transaction.category)
        assert not transaction.category

    def test_anonymous_user_cannot_add_categorisation_rule(self):
        self.client.logout()
        response = self.client.post(
            "/rules/categorization/create",
            {
                "name": "test-rule",
                "rule": '{"==": [{"var": "transaction.description"}, "food"]}',
                "effect_value": self.category.id,
            },
        )
        assert 302 == response.status_code
