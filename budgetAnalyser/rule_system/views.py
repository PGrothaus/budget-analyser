from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic

from business_logic import handlers
from rule_system.forms import CreateCategorizationRuleForm
from rule_system.models import CategorizationRule


class CategorizationRuleListView(generic.ListView):
    template_name = 'categorization/rules/list.html'

    def get_queryset(self):
        return CategorizationRule.objects.filter(user=self.request.user)


class CategorizationRuleCreateView(generic.CreateView):
    form_class = CreateCategorizationRuleForm
    template_name = 'categorization/rules/create.html'

    def get(self, request, *args, **kwarg):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            handlers.handle_rule_creation(request)
            return HttpResponseRedirect('/categorization/rules')

        return render(request, self.template_name, {'form': form})
