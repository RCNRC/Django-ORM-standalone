import os

import django
from django.utils.timezone import localtime
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

from datacenter.models import Passcard  # noqa: E402
from datacenter.models import Visit
from datacenter.models import get_duration, format_duration, is_visit_long


if __name__ == '__main__':
    # Программируем здесь
    print('Количество пропусков:', Passcard.objects.count())  # noqa: T001
    passcards = Passcard.objects.all()
    active_passcards = Passcard.objects.filter(is_active=True)
    print("Активных пропусков: ", len(active_passcards))

    non_closed_visits = Visit.objects.filter(leaved_at__isnull=True)
    print(non_closed_visits)
    for non_closed_visit in non_closed_visits:
        delta = localtime() - localtime(non_closed_visit.entered_at)
        print(non_closed_visit.leaved_at==None)
        print(f"{non_closed_visit.passcard.owner_name} зашёл в хранилище, время по Москве:\n"
              f"{localtime(non_closed_visit.entered_at)}\n\n"
              f"Находится в хранилище:\n"
              f"{delta.seconds//3600%24}:{delta.seconds//60%60}:{delta.seconds%60}")

    # print(Passcard.objects.filter(visit__entered_at__contains="")) # => Jennifer Martin
    # print(Visit.objects.filter(passcard__owner_name="Jennifer Martin"))
    visits = Visit.objects.filter(passcard__owner_name="Jennifer Martin")
    suspicion_visits = []
    for iters, visit in enumerate(visits):
        if is_visit_long(visit=visit, minutes=10):
            suspicion_visits.append(visit)
    print(f"Визиты дольше 10 мин {suspicion_visits}")

    suspicion_visits = []
    for iters, visit in enumerate(visits):
        if is_visit_long(visit=visit, minutes=1000):
            suspicion_visits.append(visit)
    print(f"Визиты дольше 1000 мин {suspicion_visits}")
