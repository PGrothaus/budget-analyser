import json
from datetime import datetime
from datetime import date
from datetime import timedelta
from dateutil.relativedelta import relativedelta

from rest_framework import serializers as core_serializers
from django.db.models import Avg
from django.db.models import Sum
from django.db.models.functions import ExtractMonth as Month
from django.db.models.functions import TruncMonth
from rest_framework import generics
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api import serializers
from backend.models import AssetValue
from backend.models import Account
from backend.models import AccountValue
from backend.models import Bank
from backend.models import Currency
from backend.models import ExchangeRate
from backend.models import Transaction
from backend.models import NetWorth
from business_logic import metrics


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

transaction_detail = TransactionViewSet.as_view({'get': 'retrieve',
                                                 'put': 'update'})


class ExchangeRateViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ExchangeRateSerializer

exchange_rate_add = ExchangeRateViewSet.as_view({'post': 'create'})


class AccountViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.AccountSerializer

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)


account_detail = AccountViewSet.as_view({'get': 'retrieve'})
account_list = AccountViewSet.as_view({'get': 'list'})


class AccountValueViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.AccountValueSerializer

    def get_queryset(self):
        return AccountValue.objects.filter(user=self.request.user)


account_value_list = AccountValueViewSet.as_view({'get': 'list'})


class BankViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.BankSerializer

    def get_queryset(self):
        return Bank.objects.filter(user=self.request.user)


bank_detail = BankViewSet.as_view({'get': 'retrieve'})


class GroupedExpensesViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.GroupedExpensesSerializer

    def get_queryset(self):
        qp = {k: v for k, v in self.request.query_params.items()}
        print(qp)
        return Transaction.objects.filter(
                user=self.request.user,
                type='expense',
                account__type=2,
                **qp
            ).exclude(
                category__group__type='neutral'
            ).values(
                'category__group__name'
            ).annotate(
                total=Sum('amount')
            ).order_by(
                '-total'
            )


expenses_grouped_detail = GroupedExpensesViewSet.as_view({'get': 'list'})


class GroupedIncomeViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.GroupedExpensesSerializer

    def get_queryset(self):
        qp = {k: v for k, v in self.request.query_params.items()}
        print(qp)
        return Transaction.objects.filter(
                user=self.request.user,
                type='income',
                account__type=2,
                **qp
            ).exclude(
                category__group__type='neutral'
            ).values(
                'category__group__name'
            ).annotate(
                total=Sum('amount')
            ).order_by(
                '-total'
            )


income_grouped_detail = GroupedIncomeViewSet.as_view({'get': 'list'})


class AverageExpensesViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.AggregateSerializer

    def get_queryset(self):
        qp = {k: v for k, v in self.request.query_params.items()}
        today = date.today()
        firstThisMonth = today.replace(day=1)
        firstLastMonth = firstThisMonth - timedelta(days=1)
        firstInitMonth = firstThisMonth - relativedelta(months=+4)
        return [Transaction.objects.filter(
                user=self.request.user,
                type='expense',
                account__type=2,
                **qp
            ).exclude(
                category__group__type='neutral'
            ).filter(
                date__gte=firstInitMonth
            ).filter(
                date__lte=firstLastMonth
            ).annotate(
                month=TruncMonth('date')
            ).values(
                'month'
            ).annotate(
                monthly_total=Sum('amount')
            ).aggregate(
                total=Avg('monthly_total')
            )
            ]


average_expenses = AverageExpensesViewSet.as_view({'get': 'list'})


class AverageIncomeViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.AggregateSerializer

    def get_queryset(self):
        qp = {k: v for k, v in self.request.query_params.items()}
        return [Transaction.objects.filter(
                user=self.request.user,
                type='income',
                account__type=2,
                **qp
            ).exclude(
                category__group__type='neutral'
            ).filter(
                date__gte=datetime.strptime("2020-02-01", "%Y-%m-%d")
            ).annotate(
                month=TruncMonth('date')
            ).values(
                'month'
            ).annotate(
                monthly_total=Sum('amount')
            ).aggregate(
                total=Avg('monthly_total')
            )
            ]


average_income = AverageIncomeViewSet.as_view({'get': 'list'})


class TotalMonthlyExpensesViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.AggregateSerializer

    def get_queryset(self):
        qp = {k: v for k, v in self.request.query_params.items()}
        return [Transaction.objects.filter(
                user=self.request.user,
                type='expense',
                account__type=2,
                **qp
            ).exclude(
                category__group__type='neutral'
            ).aggregate(
                total=Sum('amount')
            )]


monthly_expenses = TotalMonthlyExpensesViewSet.as_view({'get': 'list'})


class TotalMonthlyIncomeViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.AggregateSerializer

    def get_queryset(self):
        qp = {k: v for k, v in self.request.query_params.items()}
        return [Transaction.objects.filter(
                user=self.request.user,
                type='income',
                account__type=2,
                **qp
            ).exclude(
                category__group__type='neutral',
            ).values(
                'type'
            ).aggregate(
                total=Sum('amount')
            )]


monthly_income = TotalMonthlyIncomeViewSet.as_view({'get': 'list'})


class CompleteMonthlyIncomeViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.AggregateSerializer

    def get_queryset(self):
        qp = {k: v for k, v in self.request.query_params.items()}
        return [Transaction.objects.filter(
                user=self.request.user,
                type='income',
                **qp
            ).exclude(
                category__group__type='neutral',
            ).values(
                'type'
            ).aggregate(
                total=Sum('amount')
            )]


complete_monthly_income = CompleteMonthlyIncomeViewSet.as_view({'get': 'list'})


class TransactionFilteredView(generics.GenericAPIView,
                              mixins.ListModelMixin):
    serializer_class = serializers.TransactionSerializer

    def get_queryset(self):
        qp = {k: v for k, v in self.request.query_params.items()}
        return Transaction.objects.filter(
            user=self.request.user,
            account__type=2,
            **qp
            ).exclude(
                category__group__type='neutral'
            ).order_by(
                '-amount'
            )

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

transaction_list = TransactionFilteredView.as_view()


class CurrentAccountValuesView(generics.GenericAPIView,
                               mixins.ListModelMixin):
    serializer_class = serializers.AccountValueSerializer

    def get_queryset(self):
        acc_vals = AccountValue.objects.filter(
            user=self.request.user
            ).order_by(
                'account__name', 'account__bank__id', '-valued_at'
            ).distinct(
                'account__name', 'account__bank__id'
            )
        return self.account_values_to_target_currency(acc_vals)

    def account_values_to_target_currency(self,
                                          acc_vals,
                                          target_currency_code="CLP"):
        rates = ExchangeRate.objects.filter(
            target__code=target_currency_code
        ).order_by(
            'origin__code', 'target__code', '-valued_at'
        ).distinct(
            'origin__code', 'target__code'
        )
        target_cur = Currency.objects.get(code=target_currency_code)
        for acc_val in acc_vals:
            cur_currency_code = acc_val.account.currency.code
            if not cur_currency_code == target_currency_code:
                rate = [elem.rate for elem in rates if elem.origin.code == cur_currency_code][0]
                acc_val.account.currency = target_cur
                acc_val.value = rate * acc_val.value
        return sorted(acc_vals, key=lambda elem: elem.value, reverse=True)


    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

current_account_values = CurrentAccountValuesView.as_view()


class NetWorthView(generics.GenericAPIView,
                   mixins.ListModelMixin):
    serializer_class = serializers.AggregateSerializer

    def get_queryset(self):
        nw = NetWorth.objects.filter(
            user=self.request.user,
            type="networth"
            ).order_by('-valued_at')[0].value
        return [{"total": nw}]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

networth = NetWorthView.as_view()


class NetWorthHistoryView(generics.GenericAPIView,
                          mixins.ListModelMixin):
    serializer_class = serializers.NetworthSerializer

    def get_queryset(self):
        return NetWorth.objects.filter(
            user=self.request.user,
            type="networth"
            ).order_by('valued_at')

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

networth_history = NetWorthHistoryView.as_view()


class CurrentAssetValuesView(generics.GenericAPIView,
                             mixins.ListModelMixin):
    serializer_class = serializers.AssetValueSerializer

    def get_queryset(self):
        asset_vals = AssetValue.objects.filter(
            user=self.request.user
            ).order_by(
                'asset__name', '-valued_at'
            ).distinct(
                'asset__name'
            )
        return self.asset_values_to_target_currency(asset_vals)

    def asset_values_to_target_currency(self,
                                        asset_vals,
                                        target_currency_code="UF"):
        rates = ExchangeRate.objects.filter(
            target__code=target_currency_code
        ).order_by(
            'origin__code', 'target__code', '-valued_at'
        ).distinct(
            'origin__code', 'target__code'
        )
        target_cur = Currency.objects.get(code=target_currency_code)
        for asset_val in asset_vals:
            cur_currency_code = asset_val.asset.currency.code
            if not cur_currency_code == target_currency_code:
                rate = [elem.rate for elem in rates if elem.origin.code == cur_currency_code][0]
                asset_val.asset.currency = target_cur
                asset_val.value = rate * asset_val.value
        return sorted(asset_vals, key=lambda elem: elem.value, reverse=True)


    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

current_asset_values = CurrentAssetValuesView.as_view()
