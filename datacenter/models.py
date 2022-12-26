from django.db import models
from django.utils.timezone import localtime


def get_duration(visit):
    return localtime() - localtime(visit.entered_at)


def format_duration(duration):
    if duration.total_seconds() <= 86399:
        return f"{duration.seconds//3600}ч {duration.seconds//60%60}м"
    else:
        return f"{duration.total_seconds()//(24*3600)}д {duration.seconds//3600%24}ч {duration.seconds//60%60}м"


def is_visit_long(visit, minutes=60):
    if visit.leaved_at is not None:
        duration = visit.leaved_at - visit.entered_at
    else:
        duration = get_duration(visit)
    if duration.seconds//60 > minutes:
        return True
    return False


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard, on_delete=models.CASCADE)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return '{user} entered at {entered} {leaved}'.format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved=(
                f'leaved at {self.leaved_at}'
                if self.leaved_at else 'not leaved'
            )
        )
