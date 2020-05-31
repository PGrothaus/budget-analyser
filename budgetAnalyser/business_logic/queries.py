from django.shortcuts import get_object_or_404

from backend.models import Account
from backend.models import Bank
from backend.models import Transaction
from rule_system.models import CategorizationRule


def account_from_request(request, bank):
    return get_object_or_404(Account,
                             user_id=request.user.id,
                             bank_id=bank.id,
                             pk=request.POST['account'],
                             )


def bank_from_request(request):
    return get_object_or_404(Bank,
                             user=request.user.id,
                             pk=request.POST['bank'])


def get_uncategorized_user_transactions(request):
    return Transaction.objects.filter(user=request.user, category=None)


def insert_categorization_rule(request):
    return CategorizationRule.objects.get_or_create(name=request.POST['name'],
                                                    rule=request.POST['rule'],
                                                    effect_value_id=request.POST['effect_value'],
                                                    user=request.user)[0]


def get_all_categorization_rules(request=None):
    return CategorizationRule.objects.all()
