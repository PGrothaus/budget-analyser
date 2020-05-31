from django.contrib.postgres.fields import JSONField
from django.db import models

from backend.models import Category
from custom_auth.models import MyUser


class Rule(models.Model):

    name = models.CharField(max_length=50)
    rule = JSONField()
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)

    class Meta:
        abstract = True
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'name'],
            name='unique_rule_name_per_user')
            ]

    def __str__(self):
        return self.name


class CategorizationRule(Rule):

    effect_attribute = "category"
    effect_value = models.ForeignKey(Category, on_delete=models.CASCADE)
