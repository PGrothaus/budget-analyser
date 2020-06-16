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
                                       valued_at=datetime.now())
        print("NetWorth for user %s is %s" % (user_id, nw))


@background(schedule=1)
def collect_all_exchange_rates():
    print("Collecting rates")
    collectors.collect_all()
