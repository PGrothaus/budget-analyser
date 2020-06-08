from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from backend import views as backend_views
from api.urls import get_api_urls
from rule_system.urls import get_rule_system_urls
from dummy_frontend.urls import get_frontend_urls


# Add Admin-related urls
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += get_api_urls()
urlpatterns += get_rule_system_urls()
urlpatterns += get_frontend_urls()

# Add Account-related urls
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile', backend_views.profile, name='profile'),
]

# Add Transaction-related urls
urlpatterns += [
    path('transactions',
         login_required(backend_views.TransactionListView.as_view()),
         name='transaction_list'),
    path('transactions/uncategorized',
         login_required(backend_views.UnCategorizedTransactionListView.as_view()),
         name='transaction_uncategorized_list'),
    path('transactions/<int:pk>',
         login_required(backend_views.TransactionDetailView.as_view()),
         name='transaction_detail'),
    path('transactions/edit/<int:pk>',
         login_required(backend_views.TransactionUpdateView.as_view()),
         name='transaction_update'),
    path('transactions/upload',
         login_required(backend_views.TransactionsUploadView.as_view()),
         name='upload_transactions')
]

# Add Investment related urls
urlpatterns += [
    path('investments/input',
    login_required(backend_views.InvestmentInputView.as_view()),
    name='investment_input')
]
