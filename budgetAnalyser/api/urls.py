from django.contrib.auth.decorators import login_required
from django.urls import path
from django.urls import include

from api.views import account_detail
from api.views import account_list
from api.views import current_account_values
from api.views import current_asset_values
from api.views import bank_detail
from api.views import expenses_grouped_detail
from api.views import monthwise_expenses
from api.views import income_grouped_detail
from api.views import monthly_expenses
from api.views import monthly_income
from api.views import monthwise_income
from api.views import complete_monthly_income
from api.views import networth
from api.views import networth_history
from api.views import retirement_history
from api.views import retirement_investment_history
from api.views import savings_history
from api.views import savings_investment_history
from api.views import average_expenses
from api.views import average_income
from api.views import transaction_detail
from api.views import transaction_list
from api.views import exchange_rate_add


def get_api_urls():
    return [
        path("api/", include("rest_framework.urls")),
        path("api/accounts", account_list),
        path("api/account_values", current_account_values),
        path("api/account/<int:pk>", account_detail),
        path("api/asset_values", current_asset_values),
        path("api/bank/<int:pk>", bank_detail),
        path("api/transaction/<int:pk>", transaction_detail),
        path("api/transactions", transaction_list),
        path("api/expenses", monthly_expenses),
        path("api/expenses/average", average_expenses),
        path("api/expenses/monthwise", monthwise_expenses),
        path("api/expenses/grouped", expenses_grouped_detail),
        path("api/income/average", average_income),
        path("api/income/monthwise", monthwise_income),
        path("api/income", monthly_income),
        path("api/income/complete", complete_monthly_income),
        path("api/income/grouped", income_grouped_detail),
        path("api/networth", networth),
        path("api/networth/history", networth_history),
        path("api/retirement/history", retirement_history),
        path("api/retirement/investment/history", retirement_investment_history),
        path("api/savings/history", savings_history),
        path("api/savings/investment/history", savings_investment_history),
        path("api/exchange_rate_add", exchange_rate_add),
    ]
