import os
import json
import pytz
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.template import loader
from django.views import View
from django.views import generic
from django.views.decorators.http import require_http_methods

from business_logic import handlers
from .models import Transaction
from .models import UploadedFile
from .models import Bank
from .models import Account
from .models import Category
from .forms import InvestmentForm
from .forms import UploadTransactionsForm


@login_required
def profile(request):
    template = loader.get_template("registration/profile.html")
    context = {"user": request.user}
    return HttpResponse(template.render(context, request))


class TransactionDetailView(generic.DetailView):
    model = Transaction
    template_name = "transactions/single.html"

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)


class TransactionUpdateView(generic.UpdateView):
    model = Transaction
    fields = [
        "description",
        "amount",
        "currency",
        "date",
        "type",
        "category",
        "exclude_from_categorisation_rules",
    ]
    template_name = "transactions/update.html"

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def get_success_url(self):
        return "/transactions/uncategorized"

    def post(self, request, *args, **kwargs):
        pk = self.kwargs["pk"]
        transaction_before = Transaction.objects.get(pk=pk)
        response = super(TransactionUpdateView, self).post(request, *args, **kwargs)
        transaction_after = Transaction.objects.get(pk=pk)
        if self._updates_category(transaction_before, transaction_after):
            handlers.handle_transaction_update(request, transaction_after)
        return response

    def _updates_category(self, before, after):
        return before.category != after.category


class TransactionListView(generic.ListView):
    template_name = "transactions/list.html"

    def get_queryset(self):
        qp = self.request.GET
        qp = {key: val[0] for key, val in qp.items()}
        return Transaction.objects.filter(user=self.request.user, **qp)


class UnCategorizedTransactionListView(generic.ListView):
    template_name = "transactions/list.html"

    def get_queryset(self):
        return Transaction.objects.filter(
            user=self.request.user, category=None
        ).order_by("description")


class TransactionsUploadView(View):
    form_class = UploadTransactionsForm
    template_name = "transactions/upload.html"

    def get(self, request, *args, **kwarg):
        form = self.form_class(request.user)
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.user, request.POST, request.FILES)
        if form.is_valid():
            handlers.handle_transactions_upload(request)
            return HttpResponseRedirect("/transactions/upload")
        return render(request, self.template_name, {"form": form})


class InvestmentInputView(View):
    form_class = InvestmentForm
    template_name = "investments/input.html"

    def get(self, request, *args, **kwarg):
        form = self.form_class(request.user)
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.user, request.POST, request.FILES)
        if form.is_valid():
            handlers.handle_investment_input(request)
            return HttpResponseRedirect("/investments/input")
        return render(request, self.template_name, {"form": form})
