from datetime import datetime

from backend import models
from background_task import background
from business_logic import metrics
from collector import collectors
from custom_auth.models import MyUser


@background(schedule=1)
def calculate_networth_all_users():
    print("Calculate networth for all users...")
    user_ids = [1]
    for user_id in user_ids:
        user = MyUser.objects.get(pk=user_id)
        nw = metrics.networth(user)
        models.NetWorth.objects.create(user=user,
                                       value=nw,
                                       valued_at=datetime.now(),
                                       type="networth")
        print("NetWorth for user %s is %s" % (user_id, nw))


@background(schedule=1)
def calculate_total_retirement_all_users():
    print("Calculate total retirement for all users...")
    user_ids = [1]
    for user_id in user_ids:
        user = MyUser.objects.get(pk=user_id)
        nw = metrics.retirement(user)
        models.NetWorth.objects.create(user=user,
                                       value=nw,
                                       valued_at=datetime.now(),
                                       type="retirement")
        print("Total Retirement for user %s is %s" % (user_id, nw))


@background(schedule=1)
def calculate_total_retirement_investments_all_users():
    print("Calculate total retirement investments for all users...")
    user_ids = [1]
    for user_id in user_ids:
        user = MyUser.objects.get(pk=user_id)
        nw = metrics.retirement_investments(user)
        models.NetWorth.objects.create(user=user,
                                       value=nw,
                                       valued_at=datetime.now(),
                                       type="retirement_investment")
        print("Total Retirement Investment for user %s is %s" % (user_id, nw))


@background(schedule=1)
def calculate_savings_all_users():
    print("Calculate savings for all users...")
    user_ids = [1]
    for user_id in user_ids:
        user = MyUser.objects.get(pk=user_id)
        nw = metrics.savings(user)
        models.NetWorth.objects.create(user=user,
                                       value=nw,
                                       valued_at=datetime.now(),
                                       type="savings")
        print("All Savings for user %s is %s" % (user_id, nw))


@background(schedule=1)
def calculate_savings_investments_all_users():
    print("Calculate savings investments for all users...")
    user_ids = [1]
    for user_id in user_ids:
        user = MyUser.objects.get(pk=user_id)
        nw = metrics.savings_investments(user)
        models.NetWorth.objects.create(user=user,
                                       value=nw,
                                       valued_at=datetime.now(),
                                       type="savings_investment")
        print("All Savings Investment for user %s is %s" % (user_id, nw))


@background(schedule=1)
def collect_all_exchange_rates():
    print("Collecting rates")
    collectors.collect_all()
