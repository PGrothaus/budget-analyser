from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from backend import views as backend_views
from business_logic import tasks
from api.urls import get_api_urls
from rule_system.urls import get_rule_system_urls
from dummy_frontend.urls import get_frontend_urls
from background_task import models as task_models


# Add Admin-related urls
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

urlpatterns += get_api_urls()
urlpatterns += get_rule_system_urls()
urlpatterns += get_frontend_urls()

# Add Account-related urls
urlpatterns += [
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/profile", backend_views.profile, name="profile"),
]

# Add Transaction-related urls
urlpatterns += [
    path(
        "transactions",
        login_required(backend_views.TransactionListView.as_view()),
        name="transaction_list",
    ),
    path(
        "transactions/uncategorized",
        login_required(backend_views.UnCategorizedTransactionListView.as_view()),
        name="transaction_uncategorized_list",
    ),
    path(
        "transactions/<int:pk>",
        login_required(backend_views.TransactionDetailView.as_view()),
        name="transaction_detail",
    ),
    path(
        "transactions/edit/<int:pk>",
        login_required(backend_views.TransactionUpdateView.as_view()),
        name="transaction_update",
    ),
    path(
        "transactions/upload",
        login_required(backend_views.TransactionsUploadView.as_view()),
        name="upload_transactions",
    ),
]

# Add Investment related urls
urlpatterns += [
    path(
        "investments/input",
        login_required(backend_views.InvestmentInputView.as_view()),
        name="investment_input",
    )
]

# schedule fintual data collection
n_tasks = len(
    task_models.Task.objects.filter(
        task_name="business_logic.tasks.collect_fintual_data"
    )
)
if n_tasks == 0:
    print("scheduling fintual data collection")
    tasks.collect_fintual_data(verbose_name="Collect Fintual Data", repeat=60 * 60 * 24)

# schedule rate collection
n_tasks = len(
    task_models.Task.objects.filter(
        task_name="business_logic.tasks.collect_all_exchange_rates"
    )
)
if n_tasks == 0:
    print("scheduling exchange rate collection")
    tasks.collect_all_exchange_rates(
        verbose_name="Collect All Exchange Rates", repeat=60 * 60 * 24
    )


# schedule NW calculation
n_tasks = len(
    task_models.Task.objects.filter(
        task_name="business_logic.tasks.calculate_networth_all_users"
    )
)
if n_tasks == 0:
    print("scheduling networth calculation")
    tasks.calculate_networth_all_users(
        verbose_name="Calculate Networth All Users", repeat=60 * 60 * 24
    )


# schedule total retirement calculation
n_tasks = len(
    task_models.Task.objects.filter(
        task_name="business_logic.tasks.calculate_total_retirement_all_users"
    )
)
if n_tasks == 0:
    print("scheduling total retirement calculation")
    tasks.calculate_total_retirement_all_users(
        verbose_name="Calculate Total Retirement", repeat=60 * 60 * 24
    )

# schedule savings calculation
n_tasks = len(
    task_models.Task.objects.filter(
        task_name="business_logic.tasks.calculate_savings_all_users"
    )
)
if n_tasks == 0:
    print("scheduling savings calculation")
    tasks.calculate_savings_all_users(
        verbose_name="Calculate Savings", repeat=60 * 60 * 24
    )


# schedule total retirement investment calculation
n_tasks = len(
    task_models.Task.objects.filter(
        task_name="business_logic.tasks.calculate_total_retirement_investments_all_users"
    )
)
if n_tasks == 0:
    print("scheduling total retirement investment calculation")
    tasks.calculate_total_retirement_investments_all_users(
        verbose_name="Calculate Total Retirement Investment", repeat=60 * 60 * 24
    )

# schedule savings investment calculation
n_tasks = len(
    task_models.Task.objects.filter(
        task_name="business_logic.tasks.calculate_savings_investments_all_users"
    )
)
if n_tasks == 0:
    print("scheduling savings investment calculation")
    tasks.calculate_savings_investments_all_users(
        verbose_name="Calculate Savings Investments", repeat=60 * 60 * 24
    )
