from django.contrib.auth.decorators import login_required
from django.urls import path
from django.urls import include

from api.views import account_detail
from api.views import account_list
from api.views import current_account_values
from api.views import current_asset_values
from api.views import bank_detail
from api.views import expenses_grouped_detail
from api.views import income_grouped_detail
from api.views import monthly_expenses
from api.views import monthly_income
from api.views import networth
from api.views import average_expenses
from api.views import average_income
from api.views import transaction_detail
from api.views import transaction_list


def get_api_urls():
    API_URLS = []

    API_URLS += [
        path('api/', include('rest_framework.urls')),
        path('api/accounts', account_list),
        path('api/account_values', current_account_values),
        path('api/account/<int:pk>', account_detail),
        path('api/asset_values', current_asset_values),
        path('api/bank/<int:pk>', bank_detail),
        path('api/transaction/<int:pk>', transaction_detail),
        path('api/transactions', transaction_list),
        path('api/expenses/grouped', expenses_grouped_detail),
        path('api/income/grouped', income_grouped_detail),
        path('api/expenses', monthly_expenses),
        path('api/expenses/average', average_expenses),
        path('api/income/average', average_income),
        path('api/income', monthly_income),
        path('api/networth', networth),
    ]

    return API_URLS
