from rest_framework import serializers

from backend.models import Account
from backend.models import AccountType
from backend.models import AccountValue
from backend.models import Asset
from backend.models import AssetValue
from backend.models import Bank
from backend.models import Category
from backend.models import Currency
from backend.models import ExchangeRate
from backend.models import Transaction


class CurrencySerializer(serializers.ModelSerializer):

    class Meta:
        model = Currency
        fields = ['id', 'code', 'name']


class ExchangeRateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExchangeRate
        fields = ['id', 'origin', 'target', 'rate', 'valued_at']


class BankSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bank
        fields = ['id', 'name']


class AccountTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = AccountType
        fields = ['type']


class AccountSerializer(serializers.ModelSerializer):
    bank = BankSerializer()
    currency = CurrencySerializer()
    type = AccountTypeSerializer()

    class Meta:
        model = Account
        fields = ['id', 'name', 'bank', 'currency', 'type']
        depth = 0


class AccountValueSerializer(serializers.ModelSerializer):
    account = AccountSerializer()

    class Meta:
        model = AccountValue
        fields = ['account', 'valued_at', 'value']


class AssetSerializer(serializers.ModelSerializer):
    currency = CurrencySerializer()
    associated_credit = AccountSerializer()

    class Meta:
        model = Asset
        fields = ['name', 'type', 'currency', 'associated_credit', 'cost']


class AssetValueSerializer(serializers.ModelSerializer):
    asset = AssetSerializer()
    remaining_cost = serializers.SerializerMethodField('calc_remaining_cost')

    def calc_remaining_cost(self, obj):
        associated_credit = obj.asset.associated_credit
        if associated_credit:
            val = AccountValue.objects.filter(
                    account__id=associated_credit.id
                ).order_by(
                    '-valued_at'
                )[0]
            print("remaining credit value", val)
            return val.value
        return 100.


    class Meta:
        model = AssetValue
        fields = ['asset', 'valued_at', 'value', 'remaining_cost']


class TransactionSerializer(serializers.ModelSerializer):
    total = serializers.IntegerField(read_only=True)

    class Meta:
        model = Transaction
        fields = ['id',
                  'description',
                  'amount',
                  'currency',
                  'type',
                  'date',
                  'category',
                  'account_id',
                  'total',
                  ]
        depth = 2


class GroupedExpensesSerializer(serializers.BaseSerializer):

    def to_representation(self, data):
        return {
            'category': data["category__group__name"],
            'total': data["total"]
        }


class AggregateSerializer(serializers.BaseSerializer):

    def to_representation(self, data):
        print(data)
        return {
            'total': data["total"]
        }


class MonthwiseSerializer(serializers.BaseSerializer):

    def to_representation(self, data):
        print(data)
        return data
