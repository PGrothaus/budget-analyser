from datetime import datetime

from django.db import models
from django.contrib.auth.models import UserManager

from custom_auth.models import MyUser
from custom_auth.models import MyUserManager


class Currency(models.Model):

    code = models.CharField(max_length=10)
    name = models.CharField(max_length=30)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['code'],
            name='unique_currency_code'),
            models.UniqueConstraint(fields=['name'],
            name='unique_currency_name'),
            ]

    def __str__(self):
        return "{}: {}".format(self.pk, self.name)


class ExchangeRate(models.Model):

    origin = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='%(class)s_origin')
    target = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='%(class)s_target')
    rate = models.FloatField()
    valued_at = models.DateTimeField()

    # objects = UserManager()

    class Meta:
        indexes = [
            models.Index(fields=['origin', 'target', '-valued_at',])
        ]

    def __str__(self):
        return "1 {} to {}: {}".format(self.origin, self.target, self.rate)


class Bank(models.Model):

    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'name'],
            name='unique_bank_name_per_user')
            ]

    def __str__(self):
        return "BANK: {}".format(self.name)


class AccountType(models.Model):

    type = models.CharField(max_length=20)

    def __str__(self):
        return self.type


class Account(models.Model):

    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, default=1)
    type = models.ForeignKey(AccountType, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'bank', 'name'],
            name='unique_account_name_per_bank_per_user')
            ]

    def __str__(self):
        return "ACCOUNT: {}_{}".format(self.bank.name, self.name)


class AccountValue(models.Model):

    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    value = models.FloatField()
    valued_at = models.DateTimeField()

    class Meta:
        indexes = [
            models.Index(fields=['account', '-valued_at',])
        ]
#        constraints = [
#            models.UniqueConstraint(fields=['account_id', 'valued_at'],
#            name='unique_account_value_per_moment_in_time')
#            ]

    def __str__(self):
        return "{}: {} {}".format(self.account.name, self.value, self.account.currency.code)


class Asset(models.Model):

    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, default=1)
    type = models.CharField(max_length=20)
    cost = models.FloatField(null=True)
    associated_credit = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'name'],
            name='unique_asset_name_per_user')
            ]

    def __str__(self):
        return "ASSET: {}_{}".format(self.type, self.name)


class AssetValue(models.Model):

    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    value = models.FloatField()
    valued_at = models.DateTimeField()

    class Meta:
        indexes = [
            models.Index(fields=['asset', '-valued_at',])
        ]

    def __str__(self):
        return "{}: {} {}".format(self.asset.name, self.value, self.asset.currency.code)

class UploadedFile(models.Model):

    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField()


class CategoryGroup(models.Model):

    name = models.CharField(max_length=25, unique=True)
    type = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Category(models.Model):

    name = models.CharField(max_length=25, unique=True)
    group = models.ForeignKey(CategoryGroup, on_delete=models.CASCADE)

    def __str__(self):
        return '{}-{}-{}'.format(self.group.type, self.group.name, self.name)


class Transaction(models.Model):

    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    data_file = models.ForeignKey(UploadedFile, on_delete=models.CASCADE)
    transaction_id = models.BigIntegerField()
    description = models.CharField(max_length=200)
    amount = models.IntegerField()
    currency = models.CharField(max_length=10, default="CLP")
    type = models.CharField(max_length=10)
    date = models.DateTimeField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 blank=True, null=True)
    exclude_from_categorisation_rules = models.BooleanField(default=False)


    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'transaction_id'],
            name='unique_transaction_id_per_user')
            ]

    def __str__(self):
        return "TRANSACTION:\n  {}\n  {}\n  {}({})\n  {}({})\n {}".format(
            self.transaction_id, self.description, self.amount, self.type,
            self.account, self.date, self.category
        )


class NetWorth(models.Model):

    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    valued_at = models.DateTimeField()
    value = models.FloatField()
    type = models.CharField(max_length=40, default="networth")

    class Meta:
        constraints = [
        models.UniqueConstraint(fields=['user_id', 'valued_at'],
        name='unique_networth_per_moment_in_time')
        ]
        indexes = [
            models.Index(fields=['user_id', 'type', '-valued_at',])
        ]

    def __str__(self):
        return "{}: {}".format(self.type.capitalize(), self.value)
