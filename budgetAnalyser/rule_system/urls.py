from django.contrib.auth.decorators import login_required
from django.urls import path
from django.urls import include

from rule_system.views import CategorizationRuleListView
from rule_system.views import CategorizationRuleCreateView


def get_rule_system_urls():
    URLS = [
        path('rules/categorization',
             login_required(CategorizationRuleListView.as_view()),
             name='categorization_rule_list'),
        path('rules/categorization/create',
             login_required(CategorizationRuleCreateView.as_view()),
             name='create_rule_categorization')
    ]

    return URLS
